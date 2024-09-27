import os

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from dotenv import load_dotenv

# from api.client import APIClient
# from data.config import BASE_URLS, PAYMENT_URL, ADMIN_DB_URL

load_dotenv()
#
# api_client = APIClient(BASE_URLS)
# db_client = APIClient(ADMIN_DB_URL)
# payment_client = APIClient(PAYMENT_URL)

BOT_TOKEN = str(os.getenv("BOT_TOKEN"))

bot = Bot(token=BOT_TOKEN, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
