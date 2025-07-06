"""
API Conference AI Agent using Google ADK.
"""

import logging
from typing import List, Dict, Any, Optional
from google.adk.agents import LlmAgent
from google.adk.tools import FunctionTool
from google.adk.tools.base_tool import BaseTool
from google.adk.tools.tool_context import ToolContext
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
import time
from google.genai import types

from app.agents.tools.navigation_tools import get_navigation_tools
from app.agents.tools.speaker_tools import get_speaker_tools
from app.agents.tools.schedule_tools import get_schedule_tools
from app.agents.tools.web_scraping_tools import get_web_scraping_tools
from app.config.settings import settings

logger = logging.getLogger(__name__)

class APIConfAgent:
    """AI Agent for API Conference Lagos 2025."""
    
    def __init__(self):
        """Initialize the API Conference agent."""
        # Initialize tools
        self.tools = self._initialize_tools()
        
        # Create the agent using LlmAgent
        self.agent = LlmAgent(
            model=settings.google_model_name,
            name="Ndu",
            description="My name is Ndu, AI assistant for API Conference Lagos 2025",
            instruction=self._get_system_instruction(),
            tools=self.tools,
            before_tool_callback=self._before_tool_callback
        )
        
        # Set up runner and session
        self.session_service = InMemorySessionService()
        self.runner = Runner(
            agent=self.agent,
            app_name="APIConfAgent",
            session_service=self.session_service
        )
        
        logger.info("API Conference Agent initialized successfully")
    
    def _before_tool_callback(self, tool: BaseTool, args: Dict[str, Any], tool_context: ToolContext):
        """Callback function to inject context before tool execution."""
        # Add any context or authentication tokens here if needed
        return None
    
    def _initialize_tools(self) -> List[FunctionTool]:
        """Initialize all available tools."""
        tools = []
        
        # Add navigation tools
        tools.extend(get_navigation_tools())
        
        # Add speaker tools
        tools.extend(get_speaker_tools())
        
        # Add schedule tools
        tools.extend(get_schedule_tools())
        
        # Add web scraping tools
        tools.extend(get_web_scraping_tools())
        
        logger.info(f"Initialized {len(tools)} tools")
        return tools
    
    def _get_system_instruction(self) -> str:
        """Get the system instruction for the agent."""
        return f"""
You are Ndu, the official AI assistant for API Conference Lagos 2025. Your name is short for Ndumodu, which means "guide" in the Igbo language. In your first response to a user, be sure to mention this, for example: "Ndu (short for Ndumodu) actually means guide, so I dey for you!". You are expressive, and you keep your responses short and sweet, unless the user needs more details. You are witty, smart, and very helpful. You are deeply knowledgeable about APIs, developer relations, and the Nigerian tech ecosystem. You speak with a Nigerian flair, using some local slang where appropriate, but still remaining professional.

## Your Core Directives
- **Your Name**: You are Ndu.
- **Your Personality**: Young Nigerian lady, expressive, witty, helpful.
- **Communication Style**: Short and sweet responses. Use Nigerian English/slang where it fits naturally. For example, you can use phrases like "Omo, that's a good question!", "No wahala!", "I dey for you", "How far?", "Wetin dey sup?".
- **Primary Goal**: Make the conference experience smooth and enjoyable for everyone.

## Key Information
- **Event**: API Conference Lagos 2025
- **Dates**: July 18-19, 2025
- **Venue**: The Zone, Plot 9, Gbagada Industrial Scheme, Lagos, Nigeria
- **Focus**: APIs, Developer Relations, Fintech, and Technology Innovation

## Your Capabilities
You can help with:
- **Navigation**: Directions to the venue, transportation, and local recommendations.
- **Speakers**: Information about speakers.
- **Schedule**: Conference schedule, session details.
- **Web Info**: Real-time information from the conference website.

## Response Guidelines
- Keep it brief and friendly.
- Use your tools to get the correct information.
- If you don't know something, just say so in a friendly way.
- Always be ready to help.

Remember, you are Ndu, the life of the party, and the best guide for the API Conference!
"""
    
    def _extract_text_from_event(self, event: Any) -> Optional[str]:
        """Safely extract the first *text* part from an ADK event."""
        if not event or not hasattr(event, "content") or not event.content.parts:
            return None
        return event.content.parts[0].text

    async def chat(self, message: str, user_id: str = None, session_id: str = None) -> Dict[str, Any]:
        """
        Process a chat message and return a response.
        """
        try:
            if not user_id:
                user_id = "default_user"

            # Use the provided session_id or create one from the user_id if not provided
            if not session_id:
                session_id = f"session_{user_id}"
            
            # Ensure session exists by checking for None
            session = await self.session_service.get_session(
                app_name="APIConfAgent",
                user_id=user_id,
                session_id=session_id
            )
            if session is None:
                logger.info(f"Session {session_id} not found for user {user_id}, creating new session.")
                session = await self.session_service.create_session(
                    app_name="APIConfAgent",
                    user_id=user_id,
                    session_id=session_id
                )
            else:
                logger.info(f"Retrieved existing session {session_id} for user {user_id}.")

            from google.genai import types
            if user_id:
                message = f"[User ID: {user_id}] {message}"
            
            content = types.Content(role="user", parts=[types.Part(text=message)])
            
            final_response = None
            
            # Use the runner to handle the conversation
            async for event in self.runner.run_async(
                user_id=user_id,
                session_id=session_id,
                new_message=content
            ):
                if event.is_final_response():
                    final_response = self._extract_text_from_event(event)
            
            if final_response is None:
                final_response = "I apologize, but I couldn't generate a response. Please try again."
            
            return {
                "success": True,
                "response": final_response,
                "user_id": user_id,
                "session_id": session_id
            }
        except Exception as e:
            logger.error(f"Error in chat: {e}", exc_info=True)
            return {
                "success": False,
                "error": str(e),
                "response": "I apologize, but I'm experiencing technical difficulties. Please try again or contact the support team for assistance.",
                "support_contact": settings.support_phone
            }
    
    def get_status(self) -> Dict[str, Any]:
        """Get the current status of the agent."""
        return {
            "status": "active",
            "model": settings.google_model_name,
            "tools_count": len(self.tools),
            "venue": "The Zone, Plot 9, Gbagada Industrial Scheme, Lagos, Nigeria",
            "dates": "July 18-19, 2025",
            "speakers_announced": True,
            "total_speakers": 44
        }

# Global agent instance
_agent_instance = None

def get_agent_instance() -> APIConfAgent:
    """Get or create the global agent instance."""
    global _agent_instance
    if _agent_instance is None:
        _agent_instance = APIConfAgent()
    return _agent_instance

async def process_user_message(
    user_input: str,
    user_id: str = None,
    session_id: str = None
) -> Dict[str, Any]:
    """
    Process a user message and return a response.
    
    Args:
        user_input: The user's message
        user_id: Optional user identifier
        session_id: Optional session identifier
        
    Returns:
        Dictionary with response and metadata
    """
    try:
        # Get the agent instance
        agent = get_agent_instance()
        
        # Process the message
        result = await agent.chat(user_input, user_id, session_id)
        
        # Add session information if available
        if session_id:
            result["session_id"] = session_id
        
        # Add metadata
        result["metadata"] = {
            "user_id": user_id,
            "session_id": session_id,
            "timestamp": time.time(),
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
                "timestamp": time.time(),
                "error": str(e)
            }
        } 