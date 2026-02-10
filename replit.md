# Telegram Bot

## Overview
A Telegram bot application built with Python and the `python-telegram-bot` library (v21.3). The bot downloads chart images from elliottwave.com by category (ESTU, STU, ASTU, Cripto), packs them into ZIP archives, and sends them to users.

## Recent Changes
- 2026-02-10: /start now auto-sets yesterday's date and shows category buttons. Button press downloads images and sends ZIP archive with name format: `DD_MM_YY_CategoryName.zip`.

## Project Architecture
- `main.py` - Entry point, starts the bot
- `bot.py` - TelegramBot class with bot setup and handlers
- `handlers.py` - Message and command handlers
- `config.py` - Configuration management via environment variables
- `url_handler.py` - URL processing logic
- `urls_*.txt` - URL list files for different categories (astu, cripto, estu, stu)

## Configuration
The bot requires the following environment variables:
- `BOT_TOKEN` (required) - Telegram Bot API token
- `USE_WEBHOOK` (optional) - Enable webhook mode (default: false)
- `WEBHOOK_URL` (optional) - Webhook URL (required if USE_WEBHOOK is true)
- `WEBHOOK_PORT` (optional) - Webhook port (default: 8000)
- `LOG_LEVEL` (optional) - Logging level (default: INFO)

## Dependencies
- Python 3.11
- python-telegram-bot==21.3
- python-dotenv

## Running
The bot runs via the "Telegram Bot" workflow: `python main.py`
