"""
Web scraping tools for the API Conference AI Agent.
Handles data extraction from apiconf.net and related websites.
Uses efficient caching and follows Google ADK patterns.
"""

import asyncio
import json
from typing import Dict, Any, Optional, List
from datetime import datetime
from pathlib import Path
from google.generativeai.types import Tool

from app.config.settings import settings
from app.config.logger import Logger
from app.services.web_scraping_service import web_scraping_service

logger = Logger.get_logger(__name__)

async def scrape_apiconf_website(url: str = None, **kwargs) -> Optional[Dict[str, Any]]:
    """
    Scrape information from the API Conference website using efficient caching.
    
    Args:
        url: Optional URL to scrape (if not provided, scrapes all data)
        
    Returns:
        Dictionary with scraped information
    """
    try:
        scraped_data = await web_scraping_service.get_all_data()
        
        if url:
            # Return specific section if URL provided
            if '/speakers' in url:
                return {
                    "success": True,
                    "type": "speakers",
                    "data": scraped_data.get("speakers", {}).get("data", {}),
                    "scraped_at": datetime.now().isoformat(),
                    "support_contact": settings.support_phone
                }
            elif '/schedule' in url:
                return {
                    "success": True,
                    "type": "schedule",
                    "data": scraped_data.get("schedule", {}).get("data", {}),
                    "scraped_at": datetime.now().isoformat(),
                    "support_contact": settings.support_phone
                }
            elif '/register' in url:
                return {
                    "success": True,
                    "type": "registration",
                    "data": scraped_data.get("main", {}).get("data", {}),
                    "scraped_at": datetime.now().isoformat(),
                    "support_contact": settings.support_phone
                }
        
        # Return all data if no specific URL
        return {
            "success": True,
            "type": "all_data",
            "data": scraped_data,
            "scraped_at": datetime.now().isoformat(),
            "support_contact": settings.support_phone
        }
                
    except Exception as e:
        logger.error(f"Error scraping website: {e}")
        return {
            "error": True,
            "message": f"Failed to scrape website: {str(e)}",
            "support_contact": settings.support_phone
        }

async def get_conference_info(**kwargs) -> Optional[Dict[str, Any]]:
    """
    Get comprehensive conference information including venue, dates, and registration details.
    
    Returns:
        Dictionary with conference information
    """
    try:
        scraped_data = await web_scraping_service.get_all_data()
        
        return {
            "success": True,
            "conference_info": scraped_data.get("main", {}).get("data", {}),
            "sponsorship": scraped_data.get("main", {}).get("data", {}),
            "faqs": scraped_data.get("faq", {}).get("data", {}).get("faqs", []),
            "scraped_at": datetime.now().isoformat(),
            "support_contact": settings.support_phone
        }
                
    except Exception as e:
        logger.error(f"Error getting conference info: {e}")
        return {
            "error": True,
            "message": f"Failed to get conference information: {str(e)}",
            "support_contact": settings.support_phone
        }

async def update_conference_data(**kwargs) -> Optional[Dict[str, Any]]:
    """
    Update conference data by scraping the website and saving to local files.
    Uses efficient caching and follows Google ADK patterns.
    
    Returns:
        Dictionary with update results
    """
    try:
        scraped_data = await web_scraping_service.get_all_data()
        
        # Update local data files
        await _update_local_data_files(scraped_data)
        
        return {
            "success": True,
            "message": "Conference data updated successfully",
            "updated_at": datetime.now().isoformat(),
            "data_summary": {
                "speakers_count": len(scraped_data.get("speakers", {}).get("data", {}).get("speakers", [])),
                "schedule_days": len(scraped_data.get("schedule", {}).get("data", {}).get("schedule", [])),
                "faqs_count": len(scraped_data.get("faq", {}).get("data", {}).get("faqs", [])),
                "sponsorship_plans": 0  # Not available in current structure
            },
            "support_contact": settings.support_phone
        }
        
    except Exception as e:
        logger.error(f"Error updating conference data: {e}")
        return {
            "error": True,
            "message": "Failed to update conference data",
            "support_contact": settings.support_phone
        }

async def _update_local_data_files(scraped_data: Dict[str, Any]) -> None:
    """Update local JSON data files with scraped data."""
    try:
        # Update speakers data
        speakers_data = scraped_data.get("speakers", {}).get("data", {})
        if speakers_data and speakers_data.get("speakers"):
            speakers_file = Path("data/speakers.json")
            with open(speakers_file, 'w', encoding='utf-8') as f:
                json.dump({"speakers": speakers_data["speakers"]}, f, indent=2, ensure_ascii=False)
        
        # Update schedule data
        schedule_data = scraped_data.get("schedule", {}).get("data", {})
        if schedule_data and schedule_data.get("schedule"):
            schedule_file = Path("data/schedule.json")
            with open(schedule_file, 'w', encoding='utf-8') as f:
                json.dump({"days": [{"day": "Day 1", "sessions": schedule_data["schedule"]}]}, f, indent=2, ensure_ascii=False)
        
        logger.info("Local data files updated successfully")
        
    except Exception as e:
        logger.error(f"Error updating local data files: {e}")

def get_web_scraping_tools() -> List[Tool]:
    """Get all web scraping-related tools."""
    
    return [
        Tool(
            name="scrape_apiconf_website",
            description="Scrape information from the API Conference website using efficient caching",
            func=scrape_apiconf_website
        ),
        Tool(
            name="get_conference_info",
            description="Get comprehensive conference information including venue, dates, and registration details",
            func=get_conference_info
        ),
        Tool(
            name="update_conference_data",
            description="Update conference data by scraping the website and saving to local files",
            func=update_conference_data
        )
    ] 