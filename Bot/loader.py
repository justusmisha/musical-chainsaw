from aiogram import Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from app.api.client import APIClient
from Bot.app.bot_loader import bot
from app.data.config import BASE_URLS

api_client = APIClient('http://localhost:8000')

storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


async def set_default_commands(dp):
    await dp.bot.set_my_commands([
        types.BotCommand('menu', 'Меню'),
        types.BotCommand('start', 'Перезапустить'),
    ])