"""
Response processing service for the API Conference Agent.
"""

from typing import List, Dict, Any, Optional
import logging

from app.services.response_formatter import ResponseFormatter

logger = logging.getLogger(__name__)

class ResponseProcessor:
    """Handles processing of tool outputs and response formatting."""
    
    @staticmethod
    def process_tool_outputs(tool_outputs: List[Any]) -> Optional[str]:
        """
        Process tool outputs and format appropriate responses.
        
        Args:
            tool_outputs: List of tool output objects
            
        Returns:
            Formatted response string or None if no formatting needed
        """
        if not tool_outputs:
            return None
        
        # Debug logging
        logger.info(f"Tool outputs detected: {len(tool_outputs)}")
        logger.info(f"First tool output type: {type(tool_outputs[0])}")
        
        first_output = tool_outputs[0]
        
        # Check if the tool output is a dictionary with a 'result' key containing speaker data
        if ResponseProcessor._is_speaker_result_dict(first_output):
            logger.info("Detected speaker data, formatting response...")
            return ResponseFormatter.format_speaker_response(first_output['result'])
        
        # Check if the tool output is a dictionary with a 'result' key containing session data
        elif ResponseProcessor._is_session_result_dict(first_output):
            logger.info("Detected session data, formatting response...")
            return ResponseFormatter.format_session_response(first_output['result'])
        
        # Check if the tool output is a list of speakers
        elif ResponseProcessor._is_speaker_list(first_output):
            logger.info("Detected speaker list, formatting response...")
            return ResponseFormatter.format_speaker_response(first_output)
        
        # Check if the tool output is a list of sessions
        elif ResponseProcessor._is_session_list(first_output):
            logger.info("Detected session list, formatting response...")
            return ResponseFormatter.format_session_response(first_output)
        
        # Check if the tool output is a dictionary with session data (from search_sessions)
        elif ResponseProcessor._is_sessions_dict(first_output):
            logger.info("Detected sessions search result, formatting response...")
            return ResponseFormatter.format_session_response(first_output['sessions'])
        
        # Check if the tool output is a dictionary with speakers data (from search_speakers_csv)
        elif ResponseProcessor._is_speakers_dict(first_output):
            logger.info("Detected CSV speakers search result, formatting response...")
            return ResponseFormatter.format_speaker_response(first_output['speakers'])
        
        return None
    
    @staticmethod
    def _is_speaker_result_dict(output: Any) -> bool:
        """Check if output is a dictionary with speaker result data."""
        return (isinstance(output, dict) and 
                'result' in output and 
                isinstance(output['result'], list) and
                output['result'] and 
                isinstance(output['result'][0], dict) and
                'name' in output['result'][0] and 
                'social_links' in output['result'][0])
    
    @staticmethod
    def _is_session_result_dict(output: Any) -> bool:
        """Check if output is a dictionary with session result data."""
        return (isinstance(output, dict) and 
                'result' in output and 
                isinstance(output['result'], list) and
                output['result'] and 
                isinstance(output['result'][0], dict) and
                'title' in output['result'][0] and 
                'speakers' in output['result'][0])
    
    @staticmethod
    def _is_speaker_list(output: Any) -> bool:
        """Check if output is a list of speakers."""
        return (isinstance(output, list) and 
                all(isinstance(item, dict) for item in output) and
                output and 
                'name' in output[0] and 
                'social_links' in output[0])
    
    @staticmethod
    def _is_session_list(output: Any) -> bool:
        """Check if output is a list of sessions."""
        return (isinstance(output, list) and 
                all(isinstance(item, dict) for item in output) and
                output and 
                'title' in output[0] and 
                'speakers' in output[0])
    
    @staticmethod
    def _is_sessions_dict(output: Any) -> bool:
        """Check if output is a dictionary with sessions data."""
        return isinstance(output, dict) and 'sessions' in output
    
    @staticmethod
    def _is_speakers_dict(output: Any) -> bool:
        """Check if output is a dictionary with speakers data."""
        return isinstance(output, dict) and 'speakers' in output 