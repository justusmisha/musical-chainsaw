from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def school_menu():
    keyboard = InlineKeyboardMarkup(row=2)
    keyboard.row(
        InlineKeyboardButton(text='О школе', callback_data='about_school'),
        InlineKeyboardButton(text='Дополнительные занятия для школьников', callback_data='dop_active_school'))
    keyboard.row(
        InlineKeyboardButton(text='Продленка', callback_data='prodlenka_school'),
        InlineKeyboardButton(text='Цены', callback_data='prices_school'))
    keyboard.add(
        InlineKeyboardButton(text='Классы', callback_data='classes_school'),
        InlineKeyboardButton(text='Часто задаваемые вопросы', callback_data='faq_school'))
    keyboard.add(InlineKeyboardButton(text='Назад', callback_data='start_menu'))
    return keyboard
