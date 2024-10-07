from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from Bot.app.api.endpoints import UserEndpoints
from Bot.loader import api_client


async def school_menu() -> InlineKeyboardMarkup():
    kb = InlineKeyboardMarkup()
    kb.row(InlineKeyboardButton(text='О школе', callback_data='school_about'),
           InlineKeyboardButton(text='Кружки', callback_data='school_clubs'))
    kb.row(InlineKeyboardButton(text='Цены', callback_data='school_classes_price'),
           InlineKeyboardButton(text='Классы', callback_data='school_classes_info'))
    kb.row(InlineKeyboardButton(text='Питание', callback_data='school_food'),
           InlineKeyboardButton(text='Документы', callback_data='school_docs'))
    kb.row(InlineKeyboardButton(text='3D экскурсия', url='https://krylia-nn.ru/3d-ekskursiya-po-shkole.html'),
           InlineKeyboardButton(text='На сайт', url='https://krylia-nn.ru'))
    kb.add(InlineKeyboardButton(text='Назад', callback_data='start_menu'))
    return kb


async def school_about_kb() -> InlineKeyboardMarkup():
    kb = InlineKeyboardMarkup()
    kb.row(InlineKeyboardButton(text='Программы', callback_data='about_programs'),
           InlineKeyboardButton(text='Педагоги', callback_data='about_teachers'))
    kb.row(InlineKeyboardButton(text='Расписание', callback_data='about_schedule'),
           InlineKeyboardButton(text='Фотографии', callback_data='about_photos'))
    kb.add(InlineKeyboardButton(text='Назад', callback_data='school_start'))
    return kb


async def school_clubs() -> InlineKeyboardMarkup():
    kb = InlineKeyboardMarkup()
    all_clubs = await api_client.get(UserEndpoints.get_activities)
    if all_clubs is None:
        return None
    elif not all_clubs:
        return False
    for club in all_clubs:
        club_name = club.get('name', None)
        if club_name:
            kb.add(InlineKeyboardButton(text=club['name'], callback_data=f"school_club_{club['name']}"))
        else:
            continue
    kb.add(InlineKeyboardButton(text='Назад', callback_data='school_start'))
    return kb


async def one_activ(activ_name) -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup()
    kb.row(InlineKeyboardButton(text='Расписание', callback_data=f'school_activ_schedule_{activ_name}'),
           InlineKeyboardButton(text='Цены', callback_data=f'school_activ_price_{activ_name}'))
    kb.row(InlineKeyboardButton(text='Фотографии', callback_data=f'school_activ_photos_{activ_name}'),
           InlineKeyboardButton(text='Записаться', callback_data=f'school_activ_contact_{activ_name}'))
    kb.add(InlineKeyboardButton(text='Назад', callback_data='school_start'))
    return kb


