#!/usr/bin/env python3
"""
Daily CSV Update Script for API Conference Data
Fetches the latest data from Google Sheets and updates the local CSV file.
"""

import csv
import logging
import requests
import sys
from pathlib import Path
from datetime import datetime
from typing import Optional

# Add the project root to the path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from app.config.logger import Logger
from app.config.settings import settings

logger = Logger.get_logger(__name__)

# Local CSV file path
LOCAL_CSV_PATH = project_root / "data" / "api-conf-lagos-2025 flattened accepted sessions - exported 2025-07-05 - Accepted sessions and speakers.csv"

def fetch_csv_from_sheets() -> Optional[str]:
    """Fetch CSV data from Google Sheets."""
    try:
        logger.info("Fetching CSV data from Google Sheets...")
        response = requests.get(settings.google_sheets_url, timeout=30)
        response.raise_for_status()
        
        # Check if we got valid CSV data
        content = response.text
        if not content.strip():
            logger.error("Received empty content from Google Sheets")
            return None
            
        # Validate CSV format by trying to parse the first few lines
        lines = content.split('\n')
        if len(lines) < 2:
            logger.error("CSV content appears to be invalid (too few lines)")
            return None
            
        # Check if header looks like our expected format
        header = lines[0].lower()
        expected_columns = ['title', 'description', 'owner', 'room', 'scheduled at']
        if not all(col in header for col in expected_columns):
            logger.warning("CSV header doesn't match expected format")
            logger.info(f"Received header: {lines[0]}")
            
        logger.info(f"Successfully fetched CSV data ({len(content)} characters)")
        return content
        
    except requests.RequestException as e:
        logger.error(f"Failed to fetch CSV from Google Sheets: {e}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error fetching CSV: {e}")
        return None

def backup_existing_csv() -> bool:
    """Create a backup of the existing CSV file."""
    try:
        if not LOCAL_CSV_PATH.exists():
            logger.info("No existing CSV file to backup")
            return True
            
        # Create backup with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = LOCAL_CSV_PATH.parent / f"backup_{timestamp}_{LOCAL_CSV_PATH.name}"
        
        import shutil
        shutil.copy2(LOCAL_CSV_PATH, backup_path)
        logger.info(f"Created backup: {backup_path}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to create backup: {e}")
        return False

def update_local_csv(csv_content: str) -> bool:
    """Update the local CSV file with new content."""
    try:
        # Ensure the data directory exists
        LOCAL_CSV_PATH.parent.mkdir(parents=True, exist_ok=True)
        
        # Write the new CSV content
        with open(LOCAL_CSV_PATH, 'w', encoding='utf-8', newline='') as f:
            f.write(csv_content)
            
        logger.info(f"Successfully updated local CSV file: {LOCAL_CSV_PATH}")
        
        # Validate the written file
        with open(LOCAL_CSV_PATH, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            row_count = sum(1 for _ in reader)
            
        logger.info(f"CSV file contains {row_count} rows of data")
        return True
        
    except Exception as e:
        logger.error(f"Failed to update local CSV file: {e}")
        return False

def validate_csv_data(csv_content: str) -> bool:
    """Validate that the CSV data contains expected content."""
    try:
        lines = csv_content.split('\n')
        if len(lines) < 2:
            logger.error("CSV has insufficient data")
            return False
            
        # Parse CSV to check structure
        reader = csv.DictReader(lines)
        rows = list(reader)
        
        if not rows:
            logger.error("CSV contains no data rows")
            return False
            
        # Check for key columns
        first_row = rows[0]
        required_columns = ['Title', 'Owner', 'Scheduled At']
        missing_columns = [col for col in required_columns if col not in first_row]
        
        if missing_columns:
            logger.error(f"CSV missing required columns: {missing_columns}")
            return False
            
        # Check for some actual data
        sessions_with_titles = [row for row in rows if row.get('Title', '').strip()]
        if len(sessions_with_titles) < 10:
            logger.warning(f"CSV contains only {len(sessions_with_titles)} sessions with titles")
            
        logger.info(f"CSV validation passed: {len(rows)} total rows, {len(sessions_with_titles)} sessions")
        return True
        
    except Exception as e:
        logger.error(f"CSV validation failed: {e}")
        return False

def main():
    """Main function to update CSV data."""
    logger.info("Starting CSV update process...")
    
    # Fetch new CSV data
    csv_content = fetch_csv_from_sheets()
    if not csv_content:
        logger.error("Failed to fetch CSV data, aborting update")
        return False
    
    # Validate the fetched data
    if not validate_csv_data(csv_content):
        logger.error("CSV data validation failed, aborting update")
        return False
    
    # Create backup of existing file
    if not backup_existing_csv():
        logger.warning("Failed to create backup, but continuing with update")
    
    # Update local CSV file
    if not update_local_csv(csv_content):
        logger.error("Failed to update local CSV file")
        return False
    
    logger.info("CSV update completed successfully!")
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 