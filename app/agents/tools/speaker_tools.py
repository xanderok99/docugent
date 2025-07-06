"""
Speaker-related tools for the API Conference agent.
"""

import json
import logging
from typing import List, Dict, Any, Optional
from pathlib import Path
from google.generativeai.types import Tool

logger = logging.getLogger(__name__)

class SpeakerTools:
    """Tools for managing speaker information and queries."""
    
    def __init__(self, data_dir: str = "data"):
        """Initialize speaker tools with data directory."""
        self.data_dir = Path(data_dir)
        self.speakers_file = self.data_dir / "speakers.json"
        self._speakers_data = None
        
    def _load_speakers_data(self) -> Dict[str, Any]:
        """Load speakers data from JSON file."""
        if self._speakers_data is None:
            try:
                with open(self.speakers_file, 'r', encoding='utf-8') as f:
                    self._speakers_data = json.load(f)
                logger.info(f"Loaded {len(self._speakers_data.get('speakers', []))} speakers")
            except FileNotFoundError:
                logger.error(f"Speakers file not found: {self.speakers_file}")
                self._speakers_data = {"speakers": [], "meta": {"total_speakers": 0}}
            except json.JSONDecodeError as e:
                logger.error(f"Error parsing speakers JSON: {e}")
                self._speakers_data = {"speakers": [], "meta": {"total_speakers": 0}}
        return self._speakers_data
    
    def get_all_speakers(self) -> List[Dict[str, Any]]:
        """Get all speakers with their information."""
        data = self._load_speakers_data()
        speakers = data.get("speakers", [])
        
        # Format speaker information for display
        formatted_speakers = []
        for speaker in speakers:
            formatted_speaker = {
                "name": speaker.get("name", "Unknown"),
                "title": speaker.get("title", ""),
                "company": speaker.get("company", ""),
                "bio": speaker.get("bio", ""),
                "topics": speaker.get("topics", []),
                "status": speaker.get("status", "announced")
            }
            formatted_speakers.append(formatted_speaker)
        
        return formatted_speakers
    
    def search_speakers(self, query: str) -> List[Dict[str, Any]]:
        """Search speakers by name, company, or topics."""
        data = self._load_speakers_data()
        speakers = data.get("speakers", [])
        
        query_lower = query.lower()
        matching_speakers = []
        
        for speaker in speakers:
            # Search in name, title, company, bio, and topics
            searchable_text = [
                speaker.get("name", ""),
                speaker.get("title", ""),
                speaker.get("company", ""),
                speaker.get("bio", ""),
                *speaker.get("topics", [])
            ]
            
            if any(query_lower in text.lower() for text in searchable_text):
                formatted_speaker = {
                    "name": speaker.get("name", "Unknown"),
                    "title": speaker.get("title", ""),
                    "company": speaker.get("company", ""),
                    "bio": speaker.get("bio", ""),
                    "topics": speaker.get("topics", []),
                    "status": speaker.get("status", "announced")
                }
                matching_speakers.append(formatted_speaker)
        
        return matching_speakers
    
    def get_speaker_by_name(self, name: str) -> Optional[Dict[str, Any]]:
        """Get specific speaker information by name."""
        data = self._load_speakers_data()
        speakers = data.get("speakers", [])
        
        name_lower = name.lower()
        for speaker in speakers:
            if speaker.get("name", "").lower() == name_lower:
                return {
                    "name": speaker.get("name", "Unknown"),
                    "title": speaker.get("title", ""),
                    "company": speaker.get("company", ""),
                    "bio": speaker.get("bio", ""),
                    "topics": speaker.get("topics", []),
                    "sessions": speaker.get("sessions", []),
                    "status": speaker.get("status", "announced")
                }
        
        return None
    
    def get_speakers_by_topic(self, topic: str) -> List[Dict[str, Any]]:
        """Get speakers who specialize in a specific topic."""
        data = self._load_speakers_data()
        speakers = data.get("speakers", [])
        
        topic_lower = topic.lower()
        matching_speakers = []
        
        for speaker in speakers:
            topics = [t.lower() for t in speaker.get("topics", [])]
            if topic_lower in topics:
                formatted_speaker = {
                    "name": speaker.get("name", "Unknown"),
                    "title": speaker.get("title", ""),
                    "company": speaker.get("company", ""),
                    "bio": speaker.get("bio", ""),
                    "topics": speaker.get("topics", []),
                    "status": speaker.get("status", "announced")
                }
                matching_speakers.append(formatted_speaker)
        
        return matching_speakers
    
    def get_speakers_by_company(self, company: str) -> List[Dict[str, Any]]:
        """Get speakers from a specific company."""
        data = self._load_speakers_data()
        speakers = data.get("speakers", [])
        
        company_lower = company.lower()
        matching_speakers = []
        
        for speaker in speakers:
            if company_lower in speaker.get("company", "").lower():
                formatted_speaker = {
                    "name": speaker.get("name", "Unknown"),
                    "title": speaker.get("title", ""),
                    "company": speaker.get("company", ""),
                    "bio": speaker.get("bio", ""),
                    "topics": speaker.get("topics", []),
                    "status": speaker.get("status", "announced")
                }
                matching_speakers.append(formatted_speaker)
        
        return matching_speakers
    
    def get_speaker_statistics(self) -> Dict[str, Any]:
        """Get statistics about speakers."""
        data = self._load_speakers_data()
        speakers = data.get("speakers", [])
        meta = data.get("meta", {})
        
        # Count speakers by company type
        companies = {}
        topics = {}
        
        for speaker in speakers:
            company = speaker.get("company", "Unknown")
            companies[company] = companies.get(company, 0) + 1
            
            for topic in speaker.get("topics", []):
                topics[topic] = topics.get(topic, 0) + 1
        
        return {
            "total_speakers": len(speakers),
            "announcement_status": meta.get("announcement_status", "completed"),
            "top_companies": sorted(companies.items(), key=lambda x: x[1], reverse=True)[:10],
            "top_topics": sorted(topics.items(), key=lambda x: x[1], reverse=True)[:10],
            "last_updated": meta.get("last_updated", "Unknown")
        }

def get_speaker_tools() -> List[Tool]:
    """Get all speaker-related tools."""
    speaker_tools = SpeakerTools()
    
    return [
        Tool(
            name="get_all_speakers",
            description="Get information about all speakers at the conference",
            func=speaker_tools.get_all_speakers
        ),
        Tool(
            name="search_speakers",
            description="Search for speakers by name, company, or topics",
            func=speaker_tools.search_speakers
        ),
        Tool(
            name="get_speaker_by_name",
            description="Get detailed information about a specific speaker by name",
            func=speaker_tools.get_speaker_by_name
        ),
        Tool(
            name="get_speakers_by_topic",
            description="Find speakers who specialize in a specific topic or technology",
            func=speaker_tools.get_speakers_by_topic
        ),
        Tool(
            name="get_speakers_by_company",
            description="Find speakers from a specific company or organization",
            func=speaker_tools.get_speakers_by_company
        ),
        Tool(
            name="get_speaker_statistics",
            description="Get statistics and overview of the speaker lineup",
            func=speaker_tools.get_speaker_statistics
        )
    ] 