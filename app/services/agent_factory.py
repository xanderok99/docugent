"""
Agent factory for creating and managing API Conference Agent instances.
"""

from typing import Optional
import logging

from app.agents.apiconf_agent import APIConfAgent

logger = logging.getLogger(__name__)

class AgentFactory:
    """Factory for creating and managing agent instances."""
    
    _instance: Optional[APIConfAgent] = None
    
    @classmethod
    def get_agent_instance(cls) -> APIConfAgent:
        """Get or create the global agent instance (Singleton pattern)."""
        if cls._instance is None:
            logger.info("Creating new API Conference Agent instance")
            cls._instance = APIConfAgent()
        return cls._instance
    
    @classmethod
    def reset_instance(cls) -> None:
        """Reset the singleton instance (useful for testing)."""
        cls._instance = None
        logger.info("Reset API Conference Agent instance") 