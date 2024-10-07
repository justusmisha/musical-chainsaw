from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from Bot.app.api.endpoints import UserEndpoints
from Bot.loader import api_client


async def start_classes_menu(price: bool=False, info: bool=False) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup()
    if price:
        addit = 'price'
    else:
        addit = 'info'
    keyboard.row(InlineKeyboardButton(text='Дошкольный класс', callback_data=f'class_grad_preschool_{addit}'),
                 InlineKeyboardButton(text='Начальная школа', callback_data=f'class_grad_elementary_{addit}'))
    keyboard.row(InlineKeyboardButton(text='Средняя школа', callback_data=f'class_grad_middle_{addit}'),
                 InlineKeyboardButton(text='Старшая школа', callback_data=f'class_grad_high_{addit}'))
    keyboard.add(InlineKeyboardButton(text='Назад', callback_data='school_start'))
    return keyboard


async def get_all_classes_kb(class_grad: str) -> InlineKeyboardMarkup or bool:
    results = None
    if class_grad == 'elementary':
        results = await api_client.get(UserEndpoints.get_elementary_classes)

    elif class_grad == 'middle':
        results = await api_client.get(UserEndpoints.get_middle_classes)

    elif class_grad == 'high':
        results = await api_client.get(UserEndpoints.get_high_classes)
    print(results)
    if not results:
        return False
    elif results is None:
        return None
    kb = InlineKeyboardMarkup()
    for result in results:
        kb.add(InlineKeyboardButton(text=f"{result['class_number']}й Класс", callback_data=f"class_number_{result['class_number']}"))
    kb.add(InlineKeyboardButton(text='Назад', callback_data='school_start'))
    return kb
