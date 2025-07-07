"""
Response formatting service for the API Conference Agent.
"""

from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)

class ResponseFormatter:
    """Handles formatting of different types of responses."""
    
    @staticmethod
    def format_speaker_response(speakers: List[Dict[str, Any]]) -> str:
        """Format the response for speaker information to include profile pictures."""
        if not speakers:
            return "I couldn't find any speakers matching your query."

        response_parts = []
        for speaker in speakers:
            response_parts.append(ResponseFormatter._format_single_speaker(speaker))

        return "\n\n".join(response_parts)
    
    @staticmethod
    def _format_single_speaker(speaker: Dict[str, Any]) -> str:
        """Format a single speaker's information."""
        name = speaker.get('name', 'N/A')
        title = speaker.get('title', '')
        company = speaker.get('company', '')
        bio = speaker.get('bio', 'No bio available.')
        profile_picture = speaker.get('profile_picture')
        social_links = speaker.get('social_links', {})

        parts = []
        
        # Start with the profile picture if it exists
        if profile_picture:
            parts.append(f"![{name}]({profile_picture})")
        
        # Add name and title
        parts.append(f"### {name}")
        if title:
            parts.append(f"**{title}**")
        if company:
            parts.append(f"*{company}*")

        # Add social links
        links = []
        if 'twitter' in social_links and social_links['twitter']:
            links.append(f"[Twitter]({social_links['twitter']})")
        if 'linkedin' in social_links and social_links['linkedin']:
            links.append(f"[LinkedIn]({social_links['linkedin']})")
        if links:
            parts.append(" | ".join(links))

        # Add bio
        parts.append(f"\n{bio}\n")

        return "\n".join(parts)

    @staticmethod
    def format_session_response(sessions: List[Dict[str, Any]]) -> str:
        """Format the response for session information."""
        if not sessions:
            return "I couldn't find any sessions matching your query."

        response_parts = []
        for session in sessions:
            response_parts.append(ResponseFormatter._format_single_session(session))

        return "\n\n".join(response_parts)
    
    @staticmethod
    def _format_single_session(session: Dict[str, Any]) -> str:
        """Format a single session's information."""
        title = session.get('title', 'N/A')
        description = session.get('description', 'No description available.')
        time = session.get('time', '')
        room = session.get('room', '')
        day = session.get('day', '')
        date = session.get('date', '')
        speaker_names = session.get('speaker_names', [])
        session_type = session.get('type', 'session')
        level = session.get('level', '')

        parts = []
        
        # Add session title
        parts.append(f"### {title}")
        
        # Add session details
        details = []
        if time:
            details.append(f"**Time:** {time}")
        if room:
            details.append(f"**Room:** {room}")
        if day and date:
            details.append(f"**Date:** {day}, {date}")
        elif date:
            details.append(f"**Date:** {date}")
        if session_type:
            details.append(f"**Type:** {session_type.title()}")
        if level:
            details.append(f"**Level:** {level.title()}")
        if speaker_names:
            details.append(f"**Speaker(s):** {', '.join(speaker_names)}")
        
        if details:
            parts.append(" | ".join(details))
        
        # Add description (truncated if too long)
        if len(description) > 300:
            description = description[:300] + "..."
        parts.append(f"\n{description}\n")

        return "\n".join(parts) 