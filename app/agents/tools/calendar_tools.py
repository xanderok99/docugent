import pandas as pd
from app.schemas.agents import ToolOutput
from google.adk.tools import FunctionTool
import urllib.parse
from datetime import datetime, timedelta
import pytz

def get_session_calendar_link(session_title: str) -> ToolOutput:
    """
    Generates a Google Calendar link for a specific conference session.

    Args:
        session_title: The title of the session to get a calendar link for.

    Returns:
        A ToolOutput object containing the Google Calendar link.
    """
    try:
        df = pd.read_csv("data/api-conf-lagos-2025 flattened accepted sessions - exported 2025-07-05 - Accepted sessions and speakers.csv")
        df.columns = df.columns.str.strip()

        session = df[df['Title'].str.strip().str.lower() == session_title.strip().lower()]

        if session.empty:
            return ToolOutput(
                tool_name="get_session_calendar_link",
                raw_output=f"No session found with title: {session_title}",
                content=f"I couldn't find a session titled '{session_title}'. Please check the title and try again."
            )

        session_data = session.iloc[0]
        
        title = session_data['Title']
        description = session_data.get('Description', '')
        location = session_data.get('Room', 'The Zone, Gbagada, Lagos')
        
        scheduled_at_str = session_data['Scheduled At']
        duration_minutes = int(session_data['Scheduled Duration'])

        # Convert from WAT (UTC+1) to UTC
        wat = pytz.timezone('Africa/Lagos')
        start_time_wat = datetime.strptime(scheduled_at_str, '%d %b %Y %I:%M %p')
        start_time_wat = wat.localize(start_time_wat)
        start_time_utc = start_time_wat.astimezone(pytz.utc)
        end_time_utc = start_time_utc + timedelta(minutes=duration_minutes)

        # Format for Google Calendar URL
        start_time_str = start_time_utc.strftime('%Y%m%dT%H%M%SZ')
        end_time_str = end_time_utc.strftime('%Y%m%dT%H%M%SZ')
        
        base_url = "https://www.google.com/calendar/render?action=TEMPLATE"
        params = {
            'text': title,
            'dates': f"{start_time_str}/{end_time_str}",
            'details': description,
            'location': location
        }
        
        calendar_link = f"{base_url}&{urllib.parse.urlencode(params, safe='/')}"

        return ToolOutput(
            tool_name="get_session_calendar_link",
            raw_output=calendar_link,
            content=f"Here is the Google Calendar link for '{title}':\n[Add to Calendar]({calendar_link})"
        )

    except FileNotFoundError:
        return ToolOutput(
            tool_name="get_session_calendar_link",
            raw_output="Schedule data file not found.",
            content="I couldn't find the schedule information."
        )
    except Exception as e:
        return ToolOutput(
            tool_name="get_session_calendar_link",
            raw_output=f"An error occurred: {e}",
            content="Sorry, I encountered an error while trying to generate the calendar link."
        )

def get_calendar_tools() -> list[FunctionTool]:
    """Returns a list of tools for generating calendar links."""
    return [
        FunctionTool(get_session_calendar_link)
    ] 