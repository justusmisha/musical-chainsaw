from aiogram.types import CallbackQuery, InlineKeyboardMarkup

from Bot.app.keyboards.user.school import school_menu
from Bot.app.loaders import dp


@dp.callback_query_handler(text='school_start')
async def school_handler(call: CallbackQuery):
    kb = await school_menu()
    await call.message.edit_text(text='Подробнее о каждом из пунктов:',
                                 reply_markup=kb)


@dp.callback_query_handler(text='addit_classes_start')
async def school_handler(call: CallbackQuery):
    kb = 1
    await call.message.edit_text(text='Нажмите на занятие чтоб узнать о нем подробнее',
                                 reply_markup=await school_menu())