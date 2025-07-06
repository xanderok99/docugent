"""
Agent-specific Pydantic schemas.
"""

from typing import Optional, Dict, Any
from pydantic import BaseModel, Field

class AgentRequest(BaseModel):
    """Request schema for agent interactions."""
    message: str = Field(..., description="User message to process")
    user_id: Optional[str] = Field("anonymous", description="User identifier")
    session_id: Optional[str] = Field(None, description="Session identifier")
    context: Optional[Dict[str, Any]] = Field(None, description="Additional context")

class AgentResponse(BaseModel):
    """Response schema for agent interactions."""
    response: str = Field(..., description="Agent's response message")
    user_id: str = Field(..., description="User identifier")
    session_id: Optional[str] = Field(None, description="Session identifier")
    tools_used: Optional[list] = Field(None, description="Tools used in processing")
    confidence: Optional[float] = Field(None, description="Confidence score")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")

class AgentStatus(BaseModel):
    """Agent status information."""
    status: str = Field(..., description="Agent status")
    model: str = Field(..., description="Model being used")
    tools_available: int = Field(..., description="Number of available tools")
    uptime: str = Field(..., description="Agent uptime") 