"""
Basic tests for the API Conference AI Agent.
"""

import pytest
from unittest.mock import patch, MagicMock
from app.agents.apiconf_agent import process_user_message
from app.config.settings import settings

@pytest.mark.asyncio
async def test_agent_initialization():
    """Test that the agent can be initialized."""
    from app.agents.apiconf_agent import apiconf_agent
    assert apiconf_agent is not None

@pytest.mark.asyncio
async def test_process_user_message_success():
    """Test successful message processing."""
    with patch('app.agents.apiconf_agent.apiconf_agent.run') as mock_run:
        mock_run.return_value = "Hello! I can help you with the conference."
        
        result = await process_user_message(
            user_input="How do I get to the venue?",
            user_id="test_user"
        )
        
        assert result["success"] is True
        assert "response" in result
        mock_run.assert_called_once()

@pytest.mark.asyncio
async def test_process_user_message_error():
    """Test error handling in message processing."""
    with patch('app.agents.apiconf_agent.apiconf_agent.run') as mock_run:
        mock_run.side_effect = Exception("Test error")
        
        result = await process_user_message(
            user_input="Test message",
            user_id="test_user"
        )
        
        assert result["success"] is False
        assert "error" in result
        assert "fallback_message" in result

def test_settings_validation():
    """Test that settings are properly configured."""
    assert settings.google_model_name is not None
    assert settings.conference_venue_name is not None
    assert settings.support_phone is not None

@pytest.mark.asyncio
async def test_navigation_tools():
    """Test navigation tools functionality."""
    from app.agents.tools.navigation_tools import get_venue_access_info
    
    result = get_venue_access_info()
    
    assert "venue_name" in result
    assert "address" in result
    assert "access_notes" in result
    assert "parking_info" in result

@pytest.mark.asyncio
async def test_speaker_tools():
    """Test speaker tools functionality."""
    from app.agents.tools.speaker_tools import get_all_speakers
    
    result = get_all_speakers()
    
    assert "speakers" in result
    assert "total_count" in result 