import pandas as pd
from app.schemas.agents import ToolOutput
from google.adk.tools import FunctionTool
from typing import Optional

def get_organizer_info(query: Optional[str] = None) -> ToolOutput:
    """
    Retrieves information about the conference organizers from a CSV file.

    Args:
        query: Not used currently, but for future expansion to query specific organizers.

    Returns:
        A ToolOutput object containing a list of organizers and their roles.
    """
    try:
        # Load the CSV file
        df = pd.read_csv("data/Meet the team  - Sheet1.csv")

        # Strip any whitespace from column names
        df.columns = df.columns.str.strip()

        # Handle potential empty rows or NaN values
        df.dropna(subset=['Name', 'Role & Where you work'], inplace=True)

        # Prepare the data for output
        organizers = df[['Name', 'Role & Where you work']].to_dict('records')

        if not organizers:
            return ToolOutput(
                tool_name="get_organizer_info",
                raw_output="No organizer information found.",
                content="No organizer information found."
            )

        # Format the output
        output_str = "Here are the conference organizers:\n"
        for organizer in organizers:
            output_str += f"- {organizer['Name']}: {organizer['Role & Where you work']}\n"
        
        return ToolOutput(
            tool_name="get_organizer_info",
            raw_output=str(organizers),
            content=output_str
        )

    except FileNotFoundError:
        return ToolOutput(
            tool_name="get_organizer_info",
            raw_output="Organizer data file not found.",
            content="I couldn't find the information about the organizers."
        )
    except Exception as e:
        return ToolOutput(
            tool_name="get_organizer_info",
            raw_output=f"An error occurred: {e}",
            content="Sorry, I encountered an error while trying to get the organizer information."
        )

def get_organizer_tools() -> list[FunctionTool]:
    """Returns a list of tools for fetching organizer information."""
    return [
        FunctionTool(get_organizer_info)
    ] 