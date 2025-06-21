#!/usr/bin/env python3
"""
Main entry point for the Telegram bot application.
"""

import logging
import asyncio
from bot import TelegramBot
from config import Config

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.FileHandler('bot.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

async def main():
    """Main function to start the bot."""
    try:
        # Initialize configuration
        config = Config()
        
        # Validate configuration
        if not config.BOT_TOKEN:
            logger.error("BOT_TOKEN not found in environment variables")
            return
            
        # Initialize and start the bot
        bot = TelegramBot(config)
        logger.info("Starting Telegram bot...")
        
        await bot.start()
        
    except Exception as e:
        logger.error(f"Failed to start bot: {e}")
        raise

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Bot crashed: {e}")
