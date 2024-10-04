from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

from Bot.app.api.endpoints import UserEndpoints
from Bot.app.data.config import SCHOOL_INFO, ERROR_MESSAGE
from Bot.app.keyboards.user.school import school_about_kb, school_clubs
from Bot.loader import dp, api_client


@dp.callback_query_handler(text='school_about')
async def school_about_handler(call: CallbackQuery):
    kb = await school_about_kb()
    await call.message.edit_text(text=f'Информация о школе \n'
                                      f'{SCHOOL_INFO}',
                                 reply_markup=kb)



