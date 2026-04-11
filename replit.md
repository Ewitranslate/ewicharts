# Telegram Bot — Elliott Wave Chart Downloader

## Overview
A Telegram bot that downloads financial chart images from elliottwave.com, bundles them into ZIP archives, and sends them to users. Charts are organized into four categories: ESTU, STU, ASTU, and Cripto.

## Architecture
- **main.py** — Entry point; initializes config and starts the bot
- **bot.py** — `TelegramBot` class; sets up the python-telegram-bot application and registers handlers
- **handlers.py** — All command/callback logic (download, zip, send)
- **url_handler.py** — Loads URL templates from `.txt` files and substitutes date placeholders
- **config.py** — Reads environment variables (BOT_TOKEN, USE_WEBHOOK, etc.)
- **urls_estu.txt / urls_stu.txt / urls_astu.txt / urls_cripto.txt** — URL template files per category

## Key Dependencies
- `python-telegram-bot==21.3` — Telegram bot framework
- `httpx>=0.28.1` — Async HTTP client for downloading images
- `python-dotenv>=1.1.0` — Environment variable loading

## Configuration (Environment Variables / Secrets)
- `BOT_TOKEN` *(required secret)* — Token from Telegram @BotFather
- `USE_WEBHOOK` — `false` (default; uses long polling)
- `WEBHOOK_URL` — Required only when `USE_WEBHOOK=true`
- `WEBHOOK_PORT` — Default `8000`
- `LOG_LEVEL` — Default `INFO`

## Running
The bot runs as a long-polling Telegram bot via the "Telegram Bot" workflow (`python main.py`).
There is no web UI; interaction happens entirely through Telegram.

## Bot Commands
- `/start` — Sets date to yesterday and shows category buttons
- `/setdate DD.MM.YYYY` — Sets a custom date and shows buttons
- `/resetdate` — Resets to current date
- `/help` — Shows help message
- `/status` — Shows uptime and current settings
- `/addurl <category> <url>` — Adds a URL template to a category
- `/removeurl <category> <url>` — Removes a URL template
- `/listurl <category>` — Lists all URL templates in a category
