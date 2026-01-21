import logging
import os
from dataclasses import dataclass, field

from dotenv import load_dotenv

load_dotenv()

@dataclass
class LoggerConfig:
    """Configuration for the application logger."""
    name: str = os.getenv("LOGGER_NAME", "adk_agent")
    level: str = os.getenv("LOG_LEVEL", "DEBUG")
    format: str = os.getenv("LOG_FORMAT", "%(asctime)s - %(name)s - %(levelname)s - %(message)s")

@dataclass
class AppConfig:
    """Root configuration for the application."""
    project_id: str = os.getenv("PROJECT_ID", "")
    location: str = os.getenv("LOCATION", "us-central1")
    logger_config: LoggerConfig = field(default_factory=LoggerConfig)

config = AppConfig()

def get_logger(name: str = None) -> logging.Logger:
    """Configures and returns a logger instance."""
    if name is None:
        name = config.logger_config.name
    
    logger = logging.getLogger(name)
    
    # Only configure if handlers haven't been added yet to prevent duplication
    if not logger.handlers:
        level_str = config.logger_config.level.upper()
        level = getattr(logging, level_str, logging.INFO)
        logger.setLevel(level)
        
        handler = logging.StreamHandler()
        handler.setLevel(level)
        
        formatter = logging.Formatter(config.logger_config.format)
        handler.setFormatter(formatter)
        
        logger.addHandler(handler)
        
    return logger
