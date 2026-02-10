"""
Command and message handlers for the Telegram bot.
"""

import logging
import os
import io
import zipfile
import tempfile
from datetime import datetime, timedelta
from urllib.parse import urlparse

import httpx
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from url_handler import URLHandler

logger = logging.getLogger(__name__)

CATEGORY_NAMES = {
    'estu': 'ESTU',
    'stu': 'STU',
    'astu': 'ASTU',
    'cripto': 'Cripto'
}


class BotHandlers:
    """Collection of all bot handlers."""
    
    def __init__(self):
        """Initialize handlers."""
        self.start_time = datetime.now()
        self.url_handler = URLHandler()
        self.user_dates = {}

    def _get_yesterday_date_str(self) -> str:
        yesterday = datetime.now() - timedelta(days=1)
        return yesterday.strftime('%d.%m.%Y')

    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command — auto-set yesterday's date and show buttons."""
        try:
            user = update.effective_user
            user_id = user.id

            yesterday_str = self._get_yesterday_date_str()
            self.user_dates[user_id] = yesterday_str

            welcome_message = (
                f"Привет, {user.first_name}!\n\n"
                f"Дата автоматически установлена на вчера: {yesterday_str}\n\n"
                "Выберите категорию для скачивания графиков:"
            )

            keyboard = [
                [InlineKeyboardButton("ESTU", callback_data='estu')],
                [InlineKeyboardButton("STU", callback_data='stu')],
                [InlineKeyboardButton("ASTU", callback_data='astu')],
                [InlineKeyboardButton("Cripto", callback_data='cripto')]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)

            await update.message.reply_text(welcome_message, reply_markup=reply_markup)
            logger.info(f"Start command executed for user: {user.username or user.id}, date set to {yesterday_str}")

        except Exception as e:
            logger.error(f"Error in start command: {e}")
            await update.message.reply_text("Произошла ошибка при обработке команды /start")

    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command."""
        try:
            help_message = (
                "*Справка по боту*\n\n"
                "*Основные команды:*\n"
                "/start - Начать работу (устанавливает вчерашнюю дату)\n"
                "/help - Показать эту справку\n"
                "/about - Информация о боте\n"
                "/status - Проверить статус бота\n\n"
                "*Управление датой графиков:*\n"
                "/setdate ДД.ММ.ГГГГ - установить дату для графиков\n"
                "/resetdate - сбросить на текущую дату\n\n"
                "*Управление ссылками:*\n"
                "/addurl <категория> <ссылка> - добавить ссылку\n"
                "/removeurl <категория> <ссылка> - удалить ссылку\n"
                "/listurl <категория> - показать все ссылки\n\n"
                "*Использование:*\n"
                "Нажмите /start — бот установит вчерашнюю дату и покажет кнопки.\n"
                "Нажмите кнопку категории — бот скачает графики и отправит ZIP-архив.\n\n"
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
            uptime_str = str(uptime).split('.')[0]

            about_message = (
                "*О боте*\n\n"
                "*Название:* Telegram Bot\n"
                "*Версия:* 2.0.0\n"
                "*Язык:* Python\n"
                "*Библиотека:* python-telegram-bot\n\n"
                f"*Время работы:* {uptime_str}\n"
                f"*Запущен:* {self.start_time.strftime('%d.%m.%Y %H:%M:%S')}\n\n"
                "*Возможности:*\n"
                "- Загрузка графиков по категориям\n"
                "- Упаковка в ZIP-архивы\n"
                "- Настройка даты для графиков\n"
                "- Управление ссылками\n"
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

            current_date = self.user_dates.get(user_id, datetime.now().strftime('%d.%m.%Y'))

            status_message = (
                "*Статус бота*\n\n"
                f"Бот активен и работает\n"
                f"Время работы: {uptime_str}\n"
                f"Дата запуска: {self.start_time.strftime('%d.%m.%Y')}\n"
                f"Время запуска: {self.start_time.strftime('%H:%M:%S')}\n"
                f"Ваш ID: `{user_id}`\n"
                f"Текущая дата для графиков: {current_date}\n\n"
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

            try:
                date_obj = datetime.strptime(date_str, '%d.%m.%Y')
                self.user_dates[user_id] = date_str

                formatted_date = date_obj.strftime('%d.%m.%Y')

                keyboard = [
                    [InlineKeyboardButton("ESTU", callback_data='estu')],
                    [InlineKeyboardButton("STU", callback_data='stu')],
                    [InlineKeyboardButton("ASTU", callback_data='astu')],
                    [InlineKeyboardButton("Cripto", callback_data='cripto')]
                ]
                reply_markup = InlineKeyboardMarkup(keyboard)

                await update.message.reply_text(
                    f"Дата установлена: {formatted_date}\n\n"
                    "Выберите категорию для скачивания графиков:",
                    reply_markup=reply_markup
                )
                logger.info(f"Date set to {date_str} for user: {user_id}")

            except ValueError:
                await update.message.reply_text(
                    "Неверный формат даты!\n\n"
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
                f"Дата сброшена на текущую: {current_date}\n\n"
                "Теперь при нажатии кнопок будут загружены графики за сегодня."
            )
            logger.info(f"Date reset to current for user: {user_id}")

        except Exception as e:
            logger.error(f"Error in resetdate command: {e}")
            await update.message.reply_text("Произошла ошибка при сбросе даты")

    async def addurl_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /addurl command to add URL to category."""
        try:
            if len(context.args) < 2:
                await update.message.reply_text(
                    "Использование: /addurl <категория> <ссылка>\n\n"
                    "Категории: estu, stu, astu, cripto\n"
                    "Пример: /addurl estu https://example.com/chart{MM}{YYYY}image.png\n\n"
                    "Используйте {MM} для месяца, {YYYY} для года, {DD} для дня, {YY} для двузначного года"
                )
                return

            category = context.args[0].lower()
            url = context.args[1]

            if category not in ['estu', 'stu', 'astu', 'cripto']:
                await update.message.reply_text(
                    "Неверная категория! Доступные: estu, stu, astu, cripto"
                )
                return

            if self.url_handler.add_url_to_category(category, url):
                await update.message.reply_text(
                    f"Ссылка добавлена в категорию {category.upper()}:\n{url}"
                )
                logger.info(f"URL added to {category}: {url}")
            else:
                await update.message.reply_text(
                    f"Ошибка добавления ссылки (возможно, она уже существует)"
                )

        except Exception as e:
            logger.error(f"Error in addurl command: {e}")
            await update.message.reply_text("Произошла ошибка при добавлении ссылки")

    async def removeurl_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /removeurl command to remove URL from category."""
        try:
            if len(context.args) < 2:
                await update.message.reply_text(
                    "Использование: /removeurl <категория> <ссылка>\n\n"
                    "Категории: estu, stu, astu, cripto\n"
                    "Пример: /removeurl estu https://example.com/chart{MM}{YYYY}image.png"
                )
                return

            category = context.args[0].lower()
            url = context.args[1]

            if category not in ['estu', 'stu', 'astu', 'cripto']:
                await update.message.reply_text(
                    "Неверная категория! Доступные: estu, stu, astu, cripto"
                )
                return

            if self.url_handler.remove_url_from_category(category, url):
                await update.message.reply_text(
                    f"Ссылка удалена из категории {category.upper()}:\n{url}"
                )
                logger.info(f"URL removed from {category}: {url}")
            else:
                await update.message.reply_text(
                    f"Ссылка не найдена в категории {category.upper()}"
                )

        except Exception as e:
            logger.error(f"Error in removeurl command: {e}")
            await update.message.reply_text("Произошла ошибка при удалении ссылки")

    async def listurl_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /listurl command to list URLs in category."""
        try:
            if not context.args:
                await update.message.reply_text(
                    "Использование: /listurl <категория>\n\n"
                    "Категории: estu, stu, astu, cripto\n"
                    "Пример: /listurl estu"
                )
                return

            category = context.args[0].lower()

            if category not in ['estu', 'stu', 'astu', 'cripto']:
                await update.message.reply_text(
                    "Неверная категория! Доступные: estu, stu, astu, cripto"
                )
                return

            urls = self.url_handler.list_urls_for_category(category)

            if not urls:
                await update.message.reply_text(
                    f"Категория {category.upper()} пуста"
                )
                return

            urls_text = f"Ссылки в категории {category.upper()} ({len(urls)} шт.):\n\n"
            for i, url in enumerate(urls, 1):
                urls_text += f"{i}. {url}\n"

            if len(urls_text) > 4000:
                await update.message.reply_text(f"Категория {category.upper()} содержит {len(urls)} ссылок (слишком много для отображения)")
            else:
                await update.message.reply_text(urls_text)

        except Exception as e:
            logger.error(f"Error in listurl command: {e}")
            await update.message.reply_text("Произошла ошибка при получении списка ссылок")

    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle regular text messages."""
        try:
            user = update.effective_user
            message_text = update.message.text

            response = (
                f"Используйте /start для загрузки графиков "
                f"или /help для списка команд."
            )

            await update.message.reply_text(response)
            logger.info(f"Message processed from user {user.username or user.id}: {message_text[:50]}...")

        except Exception as e:
            logger.error(f"Error handling message: {e}")
            await update.message.reply_text(
                "Произошла ошибка при обработке вашего сообщения. Попробуйте еще раз."
            )

    async def _download_images(self, urls: list[str]) -> list[tuple[str, bytes]]:
        """Download images from URLs. Returns list of (filename, image_data)."""
        downloaded = []
        async with httpx.AsyncClient(timeout=30.0, follow_redirects=True) as client:
            for url in urls:
                try:
                    response = await client.get(url)
                    if response.status_code == 200:
                        content_type = response.headers.get('content-type', '')
                        if 'image' in content_type or url.lower().endswith(('.png', '.gif', '.jpg', '.jpeg')):
                            parsed = urlparse(url)
                            filename = os.path.basename(parsed.path)
                            if not filename:
                                filename = f"image_{len(downloaded) + 1}.png"
                            downloaded.append((filename, response.content))
                            logger.info(f"Downloaded: {filename}")
                        else:
                            logger.warning(f"Not an image (content-type: {content_type}): {url}")
                    else:
                        logger.warning(f"HTTP {response.status_code} for {url}")
                except Exception as e:
                    logger.warning(f"Failed to download {url}: {e}")
        return downloaded

    def _create_zip(self, images: list[tuple[str, bytes]], zip_name: str) -> io.BytesIO:
        """Create a ZIP archive in memory from downloaded images."""
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zf:
            seen_names = {}
            for filename, data in images:
                if filename in seen_names:
                    seen_names[filename] += 1
                    name, ext = os.path.splitext(filename)
                    filename = f"{name}_{seen_names[filename]}{ext}"
                else:
                    seen_names[filename] = 0
                zf.writestr(filename, data)
        zip_buffer.seek(0)
        return zip_buffer

    async def button_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle button callback — download images and send as ZIP."""
        try:
            query = update.callback_query
            await query.answer()

            button_data = query.data
            user = update.effective_user
            user_id = user.id
            custom_date = self.user_dates.get(user_id)

            if custom_date:
                date_parts = self.url_handler.get_custom_date_formatted(custom_date)
            else:
                date_parts = self.url_handler.get_current_date_formatted()

            date_label = f"{date_parts['DD']}.{date_parts['MM']}.20{date_parts['YY']}"
            date_for_name = f"{date_parts['DD']}_{date_parts['MM']}_{date_parts['YY']}"

            urls = self.url_handler.get_urls_for_button(button_data, custom_date)

            if not urls:
                await query.edit_message_text(text=f"Данные для {button_data.upper()} не найдены.")
                return

            category_label = CATEGORY_NAMES.get(button_data, button_data.upper())
            loading_text = f"{category_label}\n\nЗагружаю графики за {date_label}...\nВсего ссылок: {len(urls)}"
            await query.edit_message_text(text=loading_text)

            images = await self._download_images(urls)

            if not images:
                await query.edit_message_text(
                    text=f"Не удалось скачать графики для {category_label} за {date_label}.\n"
                         f"Проверено {len(urls)} ссылок — ни одна не доступна."
                )
                return

            zip_name = f"{date_for_name}_{category_label}.zip"
            zip_buffer = self._create_zip(images, zip_name)

            await query.edit_message_text(
                text=f"{category_label} за {date_label}\n"
                     f"Скачано {len(images)} из {len(urls)} графиков.\n"
                     f"Отправляю архив..."
            )

            await context.bot.send_document(
                chat_id=user_id,
                document=zip_buffer,
                filename=zip_name,
                caption=f"{category_label} — {date_label} ({len(images)} графиков)"
            )

            logger.info(f"Sent ZIP '{zip_name}' with {len(images)} images to user {user.username or user_id}")

        except Exception as e:
            logger.error(f"Error in button callback: {e}")
            try:
                await update.callback_query.edit_message_text("Произошла ошибка при загрузке графиков. Попробуйте позже.")
            except Exception:
                pass

    async def error_handler(self, update: object, context: ContextTypes.DEFAULT_TYPE):
        """Handle errors that occur during bot operation."""
        try:
            logger.error(f"Bot error: {context.error}")

            if isinstance(update, Update) and update.effective_message:
                await update.effective_message.reply_text(
                    "Произошла внутренняя ошибка. Попробуйте повторить операцию позже."
                )

        except Exception as e:
            logger.error(f"Error in error handler: {e}")
