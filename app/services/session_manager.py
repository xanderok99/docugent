"""
Session management service for the API Conference Agent.
"""

from typing import Optional
from google.adk.sessions import InMemorySessionService
import logging

logger = logging.getLogger(__name__)

class SessionManager:
    """Manages user sessions for the API Conference Agent."""
    
    def __init__(self):
        """Initialize the session manager."""
        self.session_service = InMemorySessionService()
        self.app_name = "APIConfAgent"
    
    async def get_or_create_session(self, user_id: str, session_id: str) -> any:
        """
        Get an existing session or create a new one.
        
        Args:
            user_id: The user identifier
            session_id: The session identifier
            
        Returns:
            The session object
        """
        # Ensure session exists by checking for None
        session = await self.session_service.get_session(
            app_name=self.app_name,
            user_id=user_id,
            session_id=session_id
        )
        
        if session is None:
            logger.info(f"Session {session_id} not found for user {user_id}, creating new session.")
            session = await self.session_service.create_session(
                app_name=self.app_name,
                user_id=user_id,
                session_id=session_id
            )
        else:
            logger.info(f"Retrieved existing session {session_id} for user {user_id}.")
        
        return session
    
    def get_session_service(self) -> InMemorySessionService:
        """Get the underlying session service."""
        return self.session_service 