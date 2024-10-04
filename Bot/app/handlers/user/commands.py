from aiogram import types

from Bot.app.keyboards.user.menu import start_menu
from Bot.loader import dp


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    kb = await start_menu()
    await message.answer(text='Добро пожаловать в Телеграм Бота Школы "Крылья🪽"\n'
                              'Узнайте что вас интересует прямо сейчас',
                         reply_markup=kb)


@dp.callback_query_handler(text='start_menu')
async def start(call: types.CallbackQuery):
    kb = await start_menu()
    await call.message.edit_text(text='Добро пожаловать в Телеграм Бота Школы "Крылья🪽"\n'
                                      'Узнайте что вас интересует прямо сейчас',
                                 reply_markup=kb)



