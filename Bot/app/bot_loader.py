from aiogram import Bot, types

from app.data.config import BOT_TOKEN

bot = Bot(token=BOT_TOKEN, parse_mode=types.ParseMode.HTML)