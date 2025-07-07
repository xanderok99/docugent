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
    timestamp: Optional[int] = Field(None, description="Unix ms timestamp of the user's message")
    timezone_offset: Optional[int] = Field(None, description="User's timezone offset in minutes from UTC")

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
    uptime: str = Field(..., description="Agent uptime") 