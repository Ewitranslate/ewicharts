"""
Command and message handlers for the Telegram bot.
"""

import logging
from datetime import datetime
from telegram import Update
from telegram.ext import ContextTypes

logger = logging.getLogger(__name__)

class BotHandlers:
    """Collection of all bot handlers."""
    
    def __init__(self):
        """Initialize handlers."""
        self.start_time = datetime.now()
        
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command."""
        try:
            user = update.effective_user
            welcome_message = (
                f"Привет, {user.first_name}! 👋\n\n"
                "Добро пожаловать в наш Telegram бот!\n\n"
                "Доступные команды:\n"
                "/help - Показать справку\n"
                "/about - Информация о боте\n"
                "/status - Статус бота\n\n"
                "Вы также можете отправить мне любое сообщение, и я отвечу на него."
            )
            
            await update.message.reply_text(welcome_message)
            logger.info(f"Start command executed for user: {user.username or user.id}")
            
        except Exception as e:
            logger.error(f"Error in start command: {e}")
            await update.message.reply_text("Произошла ошибка при обработке команды /start")
            
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command."""
        try:
            help_message = (
                "📖 *Справка по боту*\n\n"
                "*Доступные команды:*\n"
                "/start - Начать работу с ботом\n"
                "/help - Показать эту справку\n"
                "/about - Информация о боте\n"
                "/status - Проверить статус бота\n\n"
                "*Использование:*\n"
                "• Отправьте любое текстовое сообщение, и бот ответит\n"
                "• Используйте команды для получения информации\n"
                "• Бот автоматически обрабатывает ошибки\n\n"
                "Если у вас есть вопросы, просто напишите сообщение!"
            )
            
            await update.message.reply_text(help_message, parse_mode='Markdown')
            logger.info(f"Help command executed for user: {update.effective_user.id}")
            
        except Exception as e:
            logger.error(f"Error in help command: {e}")
            await update.message.reply_text("Произошла ошибка при обработке команды /help")
            
    async def about_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /about command."""
        try:
            uptime = datetime.now() - self.start_time
            uptime_str = str(uptime).split('.')[0]  # Remove microseconds
            
            about_message = (
                "🤖 *О боте*\n\n"
                "*Название:* Telegram Bot\n"
                "*Версия:* 1.0.0\n"
                "*Язык:* Python\n"
                "*Библиотека:* python-telegram-bot\n\n"
                f"*Время работы:* {uptime_str}\n"
                f"*Запущен:* {self.start_time.strftime('%d.%m.%Y %H:%M:%S')}\n\n"
                "*Возможности:*\n"
                "• Обработка команд\n"
                "• Ответы на сообщения\n"
                "• Логирование активности\n"
                "• Обработка ошибок\n\n"
                "Создано с ❤️ на Python"
            )
            
            await update.message.reply_text(about_message, parse_mode='Markdown')
            logger.info(f"About command executed for user: {update.effective_user.id}")
            
        except Exception as e:
            logger.error(f"Error in about command: {e}")
            await update.message.reply_text("Произошла ошибка при обработке команды /about")
            
    async def status_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /status command."""
        try:
            uptime = datetime.now() - self.start_time
            uptime_str = str(uptime).split('.')[0]
            
            status_message = (
                "✅ *Статус бота*\n\n"
                f"🟢 Бот активен и работает\n"
                f"⏱ Время работы: {uptime_str}\n"
                f"📅 Дата запуска: {self.start_time.strftime('%d.%m.%Y')}\n"
                f"🕐 Время запуска: {self.start_time.strftime('%H:%M:%S')}\n"
                f"👤 Ваш ID: `{update.effective_user.id}`\n\n"
                "Все системы функционируют нормально! 🚀"
            )
            
            await update.message.reply_text(status_message, parse_mode='Markdown')
            logger.info(f"Status command executed for user: {update.effective_user.id}")
            
        except Exception as e:
            logger.error(f"Error in status command: {e}")
            await update.message.reply_text("Произошла ошибка при обработке команды /status")
            
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle regular text messages."""
        try:
            user = update.effective_user
            message_text = update.message.text
            
            # Simple echo response with processing indicator
            response_messages = [
                f"Спасибо за сообщение, {user.first_name}! 😊",
                f"Вы написали: \"{message_text}\"",
                "Я получил ваше сообщение и обработал его.",
                "Отправьте /help для списка доступных команд."
            ]
            
            # Choose response based on message length
            if len(message_text) < 10:
                response = response_messages[0]
            elif len(message_text) < 50:
                response = response_messages[1]
            else:
                response = response_messages[2]
                
            await update.message.reply_text(response)
            
            logger.info(f"Message processed from user {user.username or user.id}: {message_text[:50]}...")
            
        except Exception as e:
            logger.error(f"Error handling message: {e}")
            await update.message.reply_text(
                "Произошла ошибка при обработке вашего сообщения. Попробуйте еще раз."
            )
            
    async def error_handler(self, update: object, context: ContextTypes.DEFAULT_TYPE):
        """Handle errors that occur during bot operation."""
        try:
            logger.error(f"Bot error: {context.error}")
            
            # Try to send error message to user if update is available
            if isinstance(update, Update) and update.effective_message:
                await update.effective_message.reply_text(
                    "Произошла внутренняя ошибка. Администратор был уведомлен. "
                    "Попробуйте повторить операцию позже."
                )
                
        except Exception as e:
            logger.error(f"Error in error handler: {e}")
