"""
API Conference AI Agent using Google ADK.
"""

import logging
from typing import List, Dict, Any
from google.generativeai import GenerativeModel
from google.generativeai.types import Tool

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
        self.model = GenerativeModel(
            model_name=settings.gemini_model,
            generation_config={
                "temperature": 0.7,
                "top_p": 0.8,
                "top_k": 40,
                "max_output_tokens": 2048,
            }
        )
        
        # Initialize tools
        self.tools = self._initialize_tools()
        
        # Create the agent
        self.agent = self.model.start_chat(
            tools=self.tools,
            system_instruction=self._get_system_instruction()
        )
        
        logger.info("API Conference Agent initialized successfully")
    
    def _initialize_tools(self) -> List[Tool]:
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
    
    async def chat(self, message: str, user_id: str = None) -> Dict[str, Any]:
        """
        Process a chat message and return a response.
        
        Args:
            message: User's message
            user_id: Optional user identifier for personalization
            
        Returns:
            Dictionary with response and metadata
        """
        try:
            # Add user context if available
            if user_id:
                message = f"[User ID: {user_id}] {message}"
            
            # Get response from agent
            response = await self.agent.send_message_async(message)
            
            # Extract tool calls if any
            tool_calls = []
            if hasattr(response, 'candidates') and response.candidates:
                candidate = response.candidates[0]
                if hasattr(candidate, 'content') and candidate.content:
                    for part in candidate.content.parts:
                        if hasattr(part, 'function_call'):
                            tool_calls.append({
                                'name': part.function_call.name,
                                'args': part.function_call.args
                            })
            
            return {
                "success": True,
                "response": response.text,
                "tool_calls": tool_calls,
                "user_id": user_id
            }
            
        except Exception as e:
            logger.error(f"Error in chat: {e}")
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
            "model": settings.gemini_model,
            "tools_count": len(self.tools),
            "venue": "The Zone, Plot 9, Gbagada Industrial Scheme, Lagos, Nigeria",
            "dates": "July 18-19, 2025",
            "speakers_announced": True,
            "total_speakers": 44
        } 