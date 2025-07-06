"""
Logging configuration for the API Conference AI Agent.
"""

import logging
import sys
from typing import Optional
from pathlib import Path

from app.config.settings import settings

class Logger:
    """Centralized logging configuration."""
    
    _loggers = {}
    
    @classmethod
    def get_logger(cls, name: str) -> logging.Logger:
        """Get or create a logger instance."""
        if name not in cls._loggers:
            logger = logging.getLogger(name)
            cls._setup_logger(logger)
            cls._loggers[name] = logger
        return cls._loggers[name]
    
    @classmethod
    def _setup_logger(cls, logger: logging.Logger) -> None:
        """Setup logger with proper configuration."""
        logger.setLevel(getattr(logging, settings.log_level.upper()))
        
        # Remove existing handlers
        logger.handlers.clear()
        
        # Create formatter
        formatter = logging.Formatter(
            fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        
        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        
        # File handler for production
        if settings.environment == "production":
            log_dir = Path("logs")
            log_dir.mkdir(exist_ok=True)
            
            file_handler = logging.FileHandler(log_dir / "apiconf_agent.log")
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
        
        # Prevent propagation to root logger
        logger.propagate = False
    
    @classmethod
    def setup_root_logger(cls) -> None:
        """Setup root logger configuration."""
        root_logger = logging.getLogger()
        root_logger.setLevel(getattr(logging, settings.log_level.upper()))
        
        # Clear existing handlers
        root_logger.handlers.clear()
        
        # Create formatter
        formatter = logging.Formatter(
            fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        
        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        root_logger.addHandler(console_handler) 