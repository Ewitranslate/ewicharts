"""
Telegram bot implementation with basic command handling and message processing.
"""

import logging
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters
from telegram import Update
from telegram.ext import ContextTypes
from handlers import BotHandlers
from config import Config

logger = logging.getLogger(__name__)

class TelegramBot:
    """Main Telegram bot class."""
    
    def __init__(self, config: Config):
        """Initialize the bot with configuration."""
        self.config = config
        self.application = None
        self.handlers = BotHandlers()
        
    async def start(self):
        """Start the bot with polling or webhook."""
        try:
            # Create application
            self.application = Application.builder().token(self.config.BOT_TOKEN).build()
            
            # Register handlers
            self._register_handlers()
            
            # Start bot
            if self.config.USE_WEBHOOK:
                await self._start_webhook()
            else:
                await self._start_polling()
                
        except Exception as e:
            logger.error(f"Error starting bot: {e}")
            raise
            
    def _register_handlers(self):
        """Register all command and message handlers."""
        try:
            # Command handlers
            self.application.add_handler(CommandHandler("start", self.handlers.start_command))
            self.application.add_handler(CommandHandler("help", self.handlers.help_command))
            self.application.add_handler(CommandHandler("about", self.handlers.about_command))
            self.application.add_handler(CommandHandler("status", self.handlers.status_command))
            self.application.add_handler(CommandHandler("setdate", self.handlers.setdate_command))
            self.application.add_handler(CommandHandler("resetdate", self.handlers.resetdate_command))
            self.application.add_handler(CommandHandler("addurl", self.handlers.addurl_command))
            self.application.add_handler(CommandHandler("removeurl", self.handlers.removeurl_command))
            self.application.add_handler(CommandHandler("listurl", self.handlers.listurl_command))
            
            # Message handlers
            self.application.add_handler(MessageHandler(
                filters.TEXT & ~filters.COMMAND, 
                self.handlers.handle_message
            ))
            
            # Callback query handler for buttons
            self.application.add_handler(CallbackQueryHandler(self.handlers.button_callback))
            
            # Error handler
            self.application.add_error_handler(self.handlers.error_handler)
            
            logger.info("All handlers registered successfully")
            
        except Exception as e:
            logger.error(f"Error registering handlers: {e}")
            raise
            
    async def _start_polling(self):
        """Start bot with polling mechanism."""
        try:
            logger.info("Starting bot with polling...")
            
            # Initialize and start the application
            await self.application.initialize()
            await self.application.start()
            
            # Start polling
            await self.application.updater.start_polling(
                drop_pending_updates=True,
                allowed_updates=Update.ALL_TYPES
            )
            
            logger.info("Bot is running with polling. Press Ctrl+C to stop.")
            
            # Keep the application running
            import asyncio
            import signal
            
            stop_signals = (signal.SIGTERM, signal.SIGINT)
            for sig in stop_signals:
                asyncio.get_event_loop().add_signal_handler(
                    sig, lambda: asyncio.create_task(self.stop())
                )
            
            # Run indefinitely until stopped
            try:
                await asyncio.Future()  # Run forever
            except asyncio.CancelledError:
                logger.info("Bot polling cancelled")
            
        except Exception as e:
            logger.error(f"Error in polling mode: {e}")
            raise
        finally:
            if self.application:
                try:
                    await self.application.stop()
                    await self.application.shutdown()
                except Exception as e:
                    logger.error(f"Error stopping application: {e}")
            
    async def _start_webhook(self):
        """Start bot with webhook mechanism."""
        try:
            logger.info("Starting bot with webhook...")
            
            # Set webhook
            webhook_url = f"{self.config.WEBHOOK_URL}/webhook"
            await self.application.bot.set_webhook(
                url=webhook_url,
                drop_pending_updates=True
            )
            
            # Start webhook server
            await self.application.run_webhook(
                listen="0.0.0.0",
                port=self.config.WEBHOOK_PORT,
                url_path="/webhook",
                webhook_url=webhook_url
            )
            
        except Exception as e:
            logger.error(f"Error in webhook mode: {e}")
            raise
            
    async def stop(self):
        """Stop the bot gracefully."""
        if self.application:
            logger.info("Stopping bot...")
            await self.application.stop()
            logger.info("Bot stopped")
