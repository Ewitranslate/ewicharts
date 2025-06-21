"""
Command and message handlers for the Telegram bot.
"""

import logging
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from url_handler import URLHandler

logger = logging.getLogger(__name__)

class BotHandlers:
    """Collection of all bot handlers."""
    
    def __init__(self):
        """Initialize handlers."""
        self.start_time = datetime.now()
        self.url_handler = URLHandler()
        
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command."""
        try:
            user = update.effective_user
            welcome_message = (
                f"Привет, {user.first_name}! 👋\n\n"
                "Добро пожаловать в наш Telegram бот!\n\n"
                "Выберите одну из опций:"
            )
            
            # Create inline keyboard with 4 buttons
            keyboard = [
                [InlineKeyboardButton("ESTU", callback_data='estu')],
                [InlineKeyboardButton("STU", callback_data='stu')],
                [InlineKeyboardButton("ASTU", callback_data='astu')],
                [InlineKeyboardButton("Cripto", callback_data='cripto')]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await update.message.reply_text(welcome_message, reply_markup=reply_markup)
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
            
    async def button_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle button callback queries."""
        try:
            query = update.callback_query
            await query.answer()
            
            button_data = query.data
            user = update.effective_user
            
            # Get URLs for the selected category
            urls = self.url_handler.get_urls_for_button(button_data)
            
            if not urls:
                await query.edit_message_text(text=f"Извините, данные для {button_data.upper()} временно недоступны.")
                return
            
            # Edit the original message to show loading
            category_names = {
                'estu': 'ESTU - Европейские рынки',
                'stu': 'STU - Американские рынки', 
                'astu': 'ASTU - Азиатские рынки',
                'cripto': 'Cripto - Криптовалютные рынки'
            }
            
            loading_text = f"{category_names.get(button_data, button_data.upper())}\n\nЗагружаю графики за {datetime.now().strftime('%d.%m.%Y')}..."
            await query.edit_message_text(text=loading_text)
            
            # Send images one by one (limit to first 10 to avoid spam)
            sent_count = 0
            max_images = 10
            
            for url in urls[:max_images]:
                try:
                    await context.bot.send_photo(
                        chat_id=query.from_user.id,
                        photo=url,
                        caption=f"График {sent_count + 1}"
                    )
                    sent_count += 1
                except Exception as img_error:
                    logger.warning(f"Failed to send image {url}: {img_error}")
                    continue
            
            # Send summary message
            if sent_count > 0:
                summary_text = f"✅ Отправлено {sent_count} графиков для {category_names.get(button_data, button_data.upper())}"
                if len(urls) > max_images:
                    summary_text += f"\n(Показаны первые {max_images} из {len(urls)} доступных)"
            else:
                summary_text = f"❌ Не удалось загрузить графики для {category_names.get(button_data, button_data.upper())}"
            
            await context.bot.send_message(
                chat_id=query.from_user.id,
                text=summary_text
            )
            
            logger.info(f"Button {button_data} pressed by user: {user.username or user.id}, sent {sent_count} images")
            
        except Exception as e:
            logger.error(f"Error in button callback: {e}")
            try:
                await update.callback_query.answer("Произошла ошибка при обработке кнопки")
            except:
                pass

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
