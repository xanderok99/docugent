"""
Tool management service for the API Conference Agent.
"""

from typing import List
from google.adk.tools import FunctionTool
from google.adk.tools.base_tool import BaseTool
from google.adk.tools.tool_context import ToolContext
import logging

from app.agents.tools.navigation_tools import get_navigation_tools
from app.agents.tools.csv_schedule_tools import get_csv_schedule_tools
from app.agents.tools.web_scraping_tools import get_web_scraping_tools
from app.agents.tools.speaker_tools import get_speaker_tools

logger = logging.getLogger(__name__)

class ToolManager:
    """Manages tool initialization and lifecycle."""
    
    def __init__(self):
        """Initialize the tool manager."""
        self._tools = None
    
    def get_tools(self) -> List[FunctionTool]:
        """Get all available tools, initializing them if necessary."""
        if self._tools is None:
            self._tools = self._initialize_tools()
        return self._tools
    
    def _initialize_tools(self) -> List[FunctionTool]:
        """Initialize all available tools."""
        tools = []
        
        # Add navigation tools
        tools.extend(get_navigation_tools())
        
        # Add CSV-based schedule tools (primary source of truth)
        tools.extend(get_csv_schedule_tools())
        
        # Add web scraping tools
        tools.extend(get_web_scraping_tools())
        
        # Add speaker tools
        tools.extend(get_speaker_tools())
        
        logger.info(f"Initialized {len(tools)} tools")
        return tools
    
    def before_tool_callback(self, tool: BaseTool, args: dict, tool_context: ToolContext):
        """Callback function to inject context before tool execution."""
        # Add any context or authentication tokens here if needed
        logger.debug(f"Executing tool: {tool.name} with args: {args}")
        return None
    
    def get_tool_count(self) -> int:
        """Get the number of available tools."""
        return len(self.get_tools()) 