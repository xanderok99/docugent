"""
Message processing service for the API Conference Agent.
"""

from typing import Optional
from datetime import datetime, timedelta, timezone
from google.genai import types
import logging

logger = logging.getLogger(__name__)

class MessageProcessor:
    """Handles message preprocessing and context injection."""
    
    @staticmethod
    def process_message(
        message: str, 
        user_id: Optional[str] = None, 
        timestamp: Optional[int] = None, 
        timezone_offset: Optional[int] = None
    ) -> types.Content:
        """
        Process and enhance a user message with context.
        
        Args:
            message: The original user message
            user_id: Optional user identifier
            timestamp: Optional user local timestamp (ms)
            timezone_offset: Optional user timezone offset (minutes)
            
        Returns:
            Enhanced message content
        """
        enhanced_message = message
        
        # Add user ID context
        if user_id:
            enhanced_message = f"[User ID: {user_id}] {enhanced_message}"
        
        # Add time context
        if timestamp and timezone_offset is not None:
            time_context = MessageProcessor._create_time_context(timestamp, timezone_offset)
            enhanced_message = f"{time_context} {enhanced_message}"
        
        # Create content object
        content = types.Content(role="user", parts=[types.Part(text=enhanced_message)])
        
        return content
    
    @staticmethod
    def _create_time_context(timestamp: int, timezone_offset: int) -> str:
        """Create time context string from timestamp and offset."""
        user_time = datetime.fromtimestamp(timestamp / 1000, tz=timezone.utc) - timedelta(minutes=timezone_offset)
        return f"[User Local Time: {user_time.strftime('%Y-%m-%d %H:%M')}, Offset: {timezone_offset}]" 