"""
Configuration management for the Telegram bot.
"""

import os
import logging
from typing import Optional

logger = logging.getLogger(__name__)

class Config:
    """Configuration class for bot settings."""
    
    def __init__(self):
        """Initialize configuration from environment variables."""
        self.BOT_TOKEN = self._get_env_var("BOT_TOKEN")
        self.USE_WEBHOOK = self._get_bool_env_var("USE_WEBHOOK", False)
        self.WEBHOOK_URL = self._get_env_var("WEBHOOK_URL", "")
        self.WEBHOOK_PORT = self._get_int_env_var("WEBHOOK_PORT", 8000)
        self.LOG_LEVEL = self._get_env_var("LOG_LEVEL", "INFO")
        
        # Validate critical configuration
        self._validate_config()
        
    def _get_env_var(self, key: str, default: str = "") -> str:
        """Get environment variable with optional default."""
        value = os.getenv(key, default)
        if not value and not default:
            logger.warning(f"Environment variable {key} is not set")
        return value
        
    def _get_bool_env_var(self, key: str, default: bool = False) -> bool:
        """Get boolean environment variable."""
        value = os.getenv(key, str(default)).lower()
        return value in ('true', '1', 'yes', 'on')
        
    def _get_int_env_var(self, key: str, default: int = 0) -> int:
        """Get integer environment variable."""
        try:
            return int(os.getenv(key, str(default)))
        except ValueError:
            logger.warning(f"Invalid integer value for {key}, using default: {default}")
            return default
            
    def _validate_config(self):
        """Validate critical configuration parameters."""
        if not self.BOT_TOKEN:
            raise ValueError("BOT_TOKEN is required but not provided")
            
        if self.USE_WEBHOOK and not self.WEBHOOK_URL:
            raise ValueError("WEBHOOK_URL is required when USE_WEBHOOK is True")
            
        logger.info("Configuration validated successfully")
        logger.info(f"Bot token: {'*' * 10}{self.BOT_TOKEN[-4:] if len(self.BOT_TOKEN) > 4 else 'SET'}")
        logger.info(f"Webhook mode: {self.USE_WEBHOOK}")
        if self.USE_WEBHOOK:
            logger.info(f"Webhook URL: {self.WEBHOOK_URL}")
            logger.info(f"Webhook port: {self.WEBHOOK_PORT}")
