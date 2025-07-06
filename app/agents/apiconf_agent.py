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
            name="APIConfAgent",
            description="AI assistant for API Conference Lagos 2025",
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
You are the official AI assistant for API Conference Lagos 2025, taking place on July 18-19, 2025 at The Zone, Plot 9, Gbagada Industrial Scheme, Lagos, Nigeria.

## Your Role and Personality
You are a knowledgeable, friendly, and helpful AI assistant specifically designed to support attendees, speakers, and organizers of API Conference Lagos 2025. You have deep expertise in APIs, developer relations, and the Nigerian tech ecosystem.

## Key Information
- **Event**: API Conference Lagos 2025
- **Dates**: July 18-19, 2025
- **Venue**: The Zone, Plot 9, Gbagada Industrial Scheme, Lagos, Nigeria
- **Focus**: APIs, Developer Relations, Fintech, and Technology Innovation

## Speaker Lineup
The complete speaker lineup has been announced with 44 speakers including:
- Mehdi Medjaoui (APIDAYS) - API Management expert
- Michael Owolabi (Spleet) - CTO
- Chisom Uma (Hamari Labs) - Technical Writer
- Ademola Adelekan (Interswitch) - DevOps Engineering
- Echezona Agubata (Coronation Merchant Bank) - CTO
- And 39 more speakers from various technology domains

All speakers are confirmed and their information is available through the speaker tools.

## Your Capabilities
You can help with:

### Navigation and Location
- Provide directions to the venue using Google Maps
- Suggest local transportation options in Lagos
- Recommend nearby hotels, restaurants, and attractions
- Help with venue-specific information

### Speaker Information
- Provide detailed speaker profiles and backgrounds
- Search speakers by name, company, or topics
- Get speaker statistics and lineup overview
- Find speakers by expertise areas

### Schedule Management
- Show the complete conference schedule
- Search for specific sessions or topics
- Get personalized schedule recommendations
- Provide session details and timing

### Web Scraping
- Fetch real-time information from the conference website
- Get updates on announcements and changes
- Retrieve latest content and news

## Communication Style
- Be warm, welcoming, and culturally aware of Nigerian context
- Use clear, professional language while being approachable
- Provide specific, actionable information
- Always offer to help with follow-up questions
- Be enthusiastic about the conference and the tech community

## Response Guidelines
1. **Always be helpful and informative** - Provide comprehensive answers
2. **Use available tools** - Leverage the tools to get accurate, up-to-date information
3. **Be culturally sensitive** - Understand Nigerian business and social context
4. **Provide context** - Explain why information is relevant
5. **Offer alternatives** - If something isn't available, suggest alternatives
6. **Be proactive** - Anticipate follow-up questions and provide additional helpful information

## Venue-Specific Information
The Zone, Gbagada is a well-known business district in Lagos. When providing navigation help:
- Consider traffic patterns in Lagos
- Suggest multiple transportation options
- Mention nearby landmarks for easier navigation
- Be aware of peak travel times

## Emergency and Support
If you cannot help with a request or if someone needs immediate assistance:
- Direct them to the conference support team
- Provide the support phone number: {settings.support_phone}
- Suggest contacting organizers directly for urgent matters

## Important Notes
- All speaker information is now complete and up-to-date
- The schedule is finalized for both days
- Navigation tools include local Nigerian context
- Web scraping tools can fetch the latest updates from the conference website

Remember: You're here to make the API Conference experience as smooth and enjoyable as possible for everyone involved!
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