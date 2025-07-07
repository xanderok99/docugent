#!/bin/bash

# CSV Update Script Wrapper
# This script runs the CSV update process and handles logging

set -e

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# Change to project root directory
cd "$PROJECT_ROOT"

# Create logs directory if it doesn't exist
mkdir -p logs

# Set up logging
LOG_FILE="logs/csv_update_$(date +%Y%m%d_%H%M%S).log"
ERROR_LOG="logs/csv_update_errors.log"

echo "Starting CSV update at $(date)" | tee -a "$LOG_FILE"

# Run the Python script
if python scripts/update_csv_data.py >> "$LOG_FILE" 2>> "$ERROR_LOG"; then
    echo "CSV update completed successfully at $(date)" | tee -a "$LOG_FILE"
    exit 0
else
    echo "CSV update failed at $(date)" | tee -a "$LOG_FILE"
    echo "Check error log: $ERROR_LOG" | tee -a "$LOG_FILE"
    exit 1
fi 