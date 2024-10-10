from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def start_menu():
    keyboard = InlineKeyboardMarkup(row=1)
    keyboard.add(InlineKeyboardButton(text='Школа', callback_data='school_start'))
    keyboard.add(InlineKeyboardButton(text='Дополнительные занятия', callback_data='addit_classes_start'))
    return keyboard