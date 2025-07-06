"""
Schedule management tools for the API Conference AI Agent.
Handles conference schedule, session information, and personalized recommendations.
"""

import json
import logging
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
from pathlib import Path
from google.adk.tools import FunctionTool

from app.config.logger import Logger
from app.config.settings import settings

logger = Logger.get_logger(__name__)

def _load_schedule_data() -> Dict[str, Any]:
    """Load schedule information from local JSON file."""
    try:
        schedule_path = Path("data/schedule.json")
        if schedule_path.exists():
            with open(schedule_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            logger.warning("schedule.json not found, using empty data")
            return {"days": []}
    except Exception as e:
        logger.error(f"Error loading schedule data: {e}")
        return {"days": []}

def get_full_schedule(**kwargs) -> Optional[Dict[str, Any]]:
    """
    Get the complete conference schedule.
    
    Returns:
        Dictionary with full schedule information
    """
    try:
        schedule_data = _load_schedule_data()
        
        return {
            "success": True,
            "schedule": schedule_data,
            "total_days": len(schedule_data.get("days", [])),
            "total_sessions": sum(
                len(day.get("sessions", [])) 
                for day in schedule_data.get("days", [])
            ),
            "support_contact": settings.support_phone
        }
        
    except Exception as e:
        logger.error(f"Error getting full schedule: {e}")
        return {
            "error": True,
            "message": "Unable to retrieve schedule",
            "support_contact": settings.support_phone
        }

def get_schedule_by_day(day: str, **kwargs) -> Optional[Dict[str, Any]]:
    """
    Get schedule for a specific day.
    
    Args:
        day: Day name (e.g., "Day 1", "Monday", "2024-03-15")
        
    Returns:
        Dictionary with day's schedule
    """
    try:
        schedule_data = _load_schedule_data()
        days = schedule_data.get("days", [])
        
        # Find the requested day
        target_day = None
        for day_data in days:
            if (day.lower() in day_data.get("day", "").lower() or
                day.lower() in day_data.get("date", "").lower()):
                target_day = day_data
                break
        
        if not target_day:
            return {
                "error": True,
                "message": f"Schedule for '{day}' not found",
                "available_days": [d.get("day") for d in days],
                "support_contact": settings.support_phone
            }
        
        return {
            "success": True,
            "day": target_day,
            "session_count": len(target_day.get("sessions", [])),
            "support_contact": settings.support_phone
        }
        
    except Exception as e:
        logger.error(f"Error getting schedule by day: {e}")
        return {
            "error": True,
            "message": "Unable to retrieve day schedule",
            "support_contact": settings.support_phone
        }

def search_sessions(query: str, **kwargs) -> Optional[Dict[str, Any]]:
    """
    Search for sessions based on title, topic, or speaker.
    
    Args:
        query: Search query
        
    Returns:
        Dictionary with matching sessions
    """
    try:
        schedule_data = _load_schedule_data()
        days = schedule_data.get("days", [])
        
        query_lower = query.lower()
        matching_sessions = []
        
        for day in days:
            for session in day.get("sessions", []):
                # Search in title, description, topics, speakers
                searchable_text = (
                    f"{session.get('title', '')} "
                    f"{session.get('description', '')} "
                    f"{' '.join(session.get('topics', []))} "
                    f"{' '.join(session.get('speakers', []))}"
                ).lower()
                
                if query_lower in searchable_text:
                    session_with_day = session.copy()
                    session_with_day["day"] = day.get("day")
                    session_with_day["date"] = day.get("date")
                    matching_sessions.append(session_with_day)
        
        return {
            "success": True,
            "query": query,
            "sessions": matching_sessions,
            "count": len(matching_sessions),
            "support_contact": settings.support_phone
        }
        
    except Exception as e:
        logger.error(f"Error searching sessions: {e}")
        return {
            "error": True,
            "message": "Unable to search sessions",
            "support_contact": settings.support_phone
        }

def recommend_schedule(user_interests: List[str], user_experience: str = "intermediate", **kwargs) -> Optional[Dict[str, Any]]:
    """
    Recommend a personalized schedule based on user interests and experience level.
    
    Args:
        user_interests: List of topics the user is interested in
        user_experience: Experience level (beginner, intermediate, advanced)
        
    Returns:
        Dictionary with recommended schedule
    """
    try:
        schedule_data = _load_schedule_data()
        days = schedule_data.get("days", [])
        
        # Load speaker data for better recommendations
        speakers_path = Path("data/speakers.json")
        speakers_data = {}
        if speakers_path.exists():
            with open(speakers_path, 'r', encoding='utf-8') as f:
                speakers_data = json.load(f)
        
        speakers = {s.get("id"): s for s in speakers_data.get("speakers", [])}
        
        recommended_sessions = []
        
        for day in days:
            day_recommendations = []
            
            for session in day.get("sessions", []):
                score = 0
                
                # Check interest match
                session_topics = session.get("topics", [])
                for interest in user_interests:
                    if interest.lower() in [topic.lower() for topic in session_topics]:
                        score += 3
                
                # Check experience level match
                session_level = session.get("level", "intermediate").lower()
                if session_level == user_experience.lower():
                    score += 2
                elif session_level in ["beginner", "intermediate"] and user_experience.lower() == "beginner":
                    score += 1
                elif session_level in ["intermediate", "advanced"] and user_experience.lower() == "advanced":
                    score += 1
                
                # Check speaker expertise
                session_speakers = session.get("speakers", [])
                for speaker_id in session_speakers:
                    speaker = speakers.get(speaker_id, {})
                    speaker_topics = speaker.get("topics", [])
                    for interest in user_interests:
                        if interest.lower() in [topic.lower() for topic in speaker_topics]:
                            score += 1
                
                if score > 0:
                    session_with_score = session.copy()
                    session_with_score["day"] = day.get("day")
                    session_with_score["date"] = day.get("date")
                    session_with_score["recommendation_score"] = score
                    day_recommendations.append(session_with_score)
            
            # Sort by score and take top recommendations per day
            day_recommendations.sort(key=lambda x: x["recommendation_score"], reverse=True)
            recommended_sessions.extend(day_recommendations[:3])  # Top 3 per day
        
        # Sort overall recommendations by score
        recommended_sessions.sort(key=lambda x: x["recommendation_score"], reverse=True)
        
        return {
            "success": True,
            "user_interests": user_interests,
            "user_experience": user_experience,
            "recommended_sessions": recommended_sessions[:10],  # Top 10 overall
            "total_recommendations": len(recommended_sessions),
            "support_contact": settings.support_phone
        }
        
    except Exception as e:
        logger.error(f"Error recommending schedule: {e}")
        return {
            "error": True,
            "message": "Unable to generate recommendations",
            "support_contact": settings.support_phone
        }

def get_session_details(session_id: str, **kwargs) -> Optional[Dict[str, Any]]:
    """
    Get detailed information about a specific session.
    
    Args:
        session_id: Unique identifier for the session
        
    Returns:
        Dictionary with session details
    """
    try:
        schedule_data = _load_schedule_data()
        days = schedule_data.get("days", [])
        
        for day in days:
            for session in day.get("sessions", []):
                if session.get("id") == session_id:
                    session_with_day = session.copy()
                    session_with_day["day"] = day.get("day")
                    session_with_day["date"] = day.get("date")
                    
                    return {
                        "success": True,
                        "session": session_with_day,
                        "support_contact": settings.support_phone
                    }
        
        return {
            "error": True,
            "message": f"Session '{session_id}' not found",
            "support_contact": settings.support_phone
        }
        
    except Exception as e:
        logger.error(f"Error getting session details: {e}")
        return {
            "error": True,
            "message": "Unable to retrieve session details",
            "support_contact": settings.support_phone
        }

def get_sessions_by_time(time_slot: str, day: Optional[str] = None, **kwargs) -> Optional[Dict[str, Any]]:
    """
    Get sessions for a specific time slot.
    
    Args:
        time_slot: Time slot (e.g., "9:00 AM", "morning", "afternoon")
        day: Optional day filter
        
    Returns:
        Dictionary with sessions in the time slot
    """
    try:
        schedule_data = _load_schedule_data()
        days = schedule_data.get("days", [])
        
        matching_sessions = []
        
        for day_data in days:
            if day and day.lower() not in day_data.get("day", "").lower():
                continue
                
            for session in day_data.get("sessions", []):
                session_time = session.get("time", "")
                if time_slot.lower() in session_time.lower():
                    session_with_day = session.copy()
                    session_with_day["day"] = day_data.get("day")
                    session_with_day["date"] = day_data.get("date")
                    matching_sessions.append(session_with_day)
        
        return {
            "success": True,
            "time_slot": time_slot,
            "day": day,
            "sessions": matching_sessions,
            "count": len(matching_sessions),
            "support_contact": settings.support_phone
        }
        
    except Exception as e:
        logger.error(f"Error getting sessions by time: {e}")
        return {
            "error": True,
            "message": "Unable to retrieve sessions by time",
            "support_contact": settings.support_phone
        }

def get_schedule_tools() -> List[FunctionTool]:
    """Get all schedule-related tools."""
    
    return [
        FunctionTool(get_full_schedule),
        FunctionTool(get_schedule_by_day),
        FunctionTool(search_sessions),
        FunctionTool(recommend_schedule),
        FunctionTool(get_session_details),
        FunctionTool(get_sessions_by_time)
    ] 