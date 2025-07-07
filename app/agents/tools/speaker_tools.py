"""
Speaker-related tools for the API Conference Agent.
"""

from typing import List, Dict, Any
from google.adk.tools import FunctionTool
import logging

logger = logging.getLogger(__name__)

def get_speaker_tools() -> List[FunctionTool]:
    """Get speaker-related tools."""
    # This is a placeholder - speaker functionality is currently handled by CSV tools
    # In the future, this could include speaker-specific tools like:
    # - Speaker availability checking
    # - Speaker contact information
    # - Speaker session scheduling
    return []

class SpeakerTools:
    """Speaker-related utility functions."""
    
    @staticmethod
    def format_speaker_profile(speaker: Dict[str, Any]) -> str:
        """Format a speaker's profile information."""
        name = speaker.get('name', 'N/A')
        title = speaker.get('title', '')
        company = speaker.get('company', '')
        bio = speaker.get('bio', 'No bio available.')
        profile_picture = speaker.get('profile_picture')
        social_links = speaker.get('social_links', {})

        parts = []
        
        if profile_picture:
            parts.append(f"![{name}]({profile_picture})")
        
        parts.append(f"### {name}")
        if title:
            parts.append(f"**{title}**")
        if company:
            parts.append(f"*{company}*")

        links = []
        if 'twitter' in social_links and social_links['twitter']:
            links.append(f"[Twitter]({social_links['twitter']})")
        if 'linkedin' in social_links and social_links['linkedin']:
            links.append(f"[LinkedIn]({social_links['linkedin']})")
        if links:
            parts.append(" | ".join(links))

        parts.append(f"\n{bio}\n")
        
        return "\n".join(parts) 