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
        self.user_dates = {}  # Store custom dates for users
        
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
                "*Основные команды:*\n"
                "/start - Начать работу с ботом\n"
                "/help - Показать эту справку\n"
                "/about - Информация о боте\n"
                "/status - Проверить статус бота\n\n"
                "*Управление датой графиков:*\n"
                "/setdate ДД.ММ.ГГГГ - установить дату для графиков\n"
                "/resetdate - сбросить на текущую дату\n\n"
                "*Использование:*\n"
                "• Нажмите /start чтобы увидеть кнопки выбора рынков\n"
                "• Используйте /setdate для просмотра графиков за определенную дату\n"
                "• Графики обновляются автоматически по заданной дате\n\n"
                "Пример: /setdate 15.06.2025"
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
            user_id = update.effective_user.id
            
            # Get current date setting for user
            current_date = self.user_dates.get(user_id, datetime.now().strftime('%d.%m.%Y'))
            
            status_message = (
                "✅ *Статус бота*\n\n"
                f"🟢 Бот активен и работает\n"
                f"⏱ Время работы: {uptime_str}\n"
                f"📅 Дата запуска: {self.start_time.strftime('%d.%m.%Y')}\n"
                f"🕐 Время запуска: {self.start_time.strftime('%H:%M:%S')}\n"
                f"👤 Ваш ID: `{user_id}`\n"
                f"📊 Текущая дата для графиков: {current_date}\n\n"
                "Команды:\n"
                "/setdate ДД.ММ.ГГГГ - установить дату для графиков\n"
                "/resetdate - сбросить на текущую дату\n\n"
                "Все системы функционируют нормально!"
            )
            
            await update.message.reply_text(status_message, parse_mode='Markdown')
            logger.info(f"Status command executed for user: {user_id}")
            
        except Exception as e:
            logger.error(f"Error in status command: {e}")
            await update.message.reply_text("Произошла ошибка при обработке команды /status")

    async def setdate_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /setdate command to set custom date."""
        try:
            user_id = update.effective_user.id
            
            if not context.args:
                await update.message.reply_text(
                    "Использование: /setdate ДД.ММ.ГГГГ\n\n"
                    "Пример: /setdate 15.06.2025\n"
                    "Эта дата будет использоваться для загрузки графиков"
                )
                return
            
            date_str = context.args[0]
            
            # Validate date format
            try:
                date_obj = datetime.strptime(date_str, '%d.%m.%Y')
                self.user_dates[user_id] = date_str
                
                formatted_date = date_obj.strftime('%d.%m.%Y')
                await update.message.reply_text(
                    f"✅ Дата установлена: {formatted_date}\n\n"
                    "Теперь при нажатии кнопок будут загружены графики за эту дату.\n"
                    "Используйте /resetdate для возврата к текущей дате."
                )
                logger.info(f"Date set to {date_str} for user: {user_id}")
                
            except ValueError:
                await update.message.reply_text(
                    "❌ Неверный формат даты!\n\n"
                    "Используйте формат: ДД.ММ.ГГГГ\n"
                    "Пример: 15.06.2025"
                )
                
        except Exception as e:
            logger.error(f"Error in setdate command: {e}")
            await update.message.reply_text("Произошла ошибка при установке даты")

    async def resetdate_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /resetdate command to reset to current date."""
        try:
            user_id = update.effective_user.id
            
            if user_id in self.user_dates:
                del self.user_dates[user_id]
            
            current_date = datetime.now().strftime('%d.%m.%Y')
            await update.message.reply_text(
                f"✅ Дата сброшена на текущую: {current_date}\n\n"
                "Теперь при нажатии кнопок будут загружены графики за сегодня."
            )
            logger.info(f"Date reset to current for user: {user_id}")
            
        except Exception as e:
            logger.error(f"Error in resetdate command: {e}")
            await update.message.reply_text("Произошла ошибка при сбросе даты")
            
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
            
            # Get URLs for the selected category with user's custom date if set
            user_id = user.id
            custom_date = self.user_dates.get(user_id)
            urls = self.url_handler.get_urls_for_button(button_data, custom_date)
            
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
            
            display_date = custom_date if custom_date else datetime.now().strftime('%d.%m.%Y')
            loading_text = f"{category_names.get(button_data, button_data.upper())}\n\nЗагружаю графики за {display_date}..."
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
