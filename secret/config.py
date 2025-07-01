import os
from dotenv import load_dotenv

from aiogram.enums.parse_mode import ParseMode
from aiogram.client.bot import DefaultBotProperties

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
BOT_PROPERTIES = DefaultBotProperties(parse_mode=ParseMode.HTML)
