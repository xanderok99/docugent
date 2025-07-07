"""
Public API for the API Conference Agent.
"""

import time
import logging
from typing import Dict, Any

from app.services.agent_factory import AgentFactory

logger = logging.getLogger(__name__)

async def process_user_message(
    user_input: str,
    user_id: str = None,
    session_id: str = None,
    timestamp: int = None,
    timezone_offset: int = None
) -> Dict[str, Any]:
    """
    Process a user message and return a response.
    
    Args:
        user_input: The user's message
        user_id: Optional user identifier
        session_id: Optional session identifier
        timestamp: Optional user local timestamp (ms)
        timezone_offset: Optional user timezone offset (minutes)
        
    Returns:
        Dictionary with response and metadata
    """
    try:
        # Get the agent instance
        agent = AgentFactory.get_agent_instance()
        
        # Process the message
        result = await agent.chat(user_input, user_id, session_id, timestamp=timestamp, timezone_offset=timezone_offset)
        
        # Add session information if available
        if session_id:
            result["session_id"] = session_id
        
        # Add metadata
        result["metadata"] = {
            "user_id": user_id,
            "session_id": session_id,
            "timestamp": timestamp or time.time(),
            "timezone_offset": timezone_offset,
            "tools_used": result.get("tool_calls", [])
        }
        
        # Add confidence score (simplified)
        result["confidence"] = 0.9 if result.get("success") else 0.1
        
        return result
        
    except Exception as e:
        logger.error(f"Error processing user message: {e}")
        return {
            "success": False,
            "response": "I apologize, but I'm experiencing technical difficulties. Please try again or contact the support team for assistance.",
            "fallback_message": "Agent processing failed",
            "error": str(e),
            "user_id": user_id,
            "session_id": session_id,
            "confidence": 0.0,
            "tools_used": [],
            "metadata": {
                "user_id": user_id,
                "session_id": session_id,
                "timestamp": timestamp or time.time(),
                "timezone_offset": timezone_offset,
                "error": str(e)
            }
        }

def get_agent_status() -> Dict[str, Any]:
    """Get the current status of the agent."""
    try:
        agent = AgentFactory.get_agent_instance()
        return agent.get_status()
    except Exception as e:
        logger.error(f"Error getting agent status: {e}")
        return {
            "status": "error",
            "error": str(e)
        } 