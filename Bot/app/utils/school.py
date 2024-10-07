from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from Bot.app.api.endpoints import UserEndpoints
from Bot.app.data import config
from Bot.loader import api_client


async def get_class_info(class_number: int):
    result = await api_client.get(UserEndpoints.get_class_by_number, class_number=class_number)
    if not result:
        return False
    elif result is None:
        return None
    else:
        json_schedule = result['schedule']
        enter = '\n'
        text = (f"<b>Информация о {class_number} классе</b>\n\n"
                f"Оставшихся мест: {result['left_places']}\n\n"
                f"Расписание\n{enter.join(f'{key.capitalize()} : {value}' for key, value in json_schedule.items())}\n\n"
                f"Записаться на встречу\n{config.SCHOOL_CONTACT_NUMBER}"
                )
        kb = InlineKeyboardMarkup()
        kb.add(InlineKeyboardButton(text='Преподаватели', callback_data=f'teachers_class_{class_number}'))
        kb.add(InlineKeyboardButton(text='Назад', callback_data=f'school_start'))

        return text, kb


async def get_grad_info(class_grad: str):
    results = None
    if class_grad == 'elementary':
        results = await api_client.get(UserEndpoints.get_elementary_classes)

    elif class_grad == 'middle':
        results = await api_client.get(UserEndpoints.get_middle_classes)

    elif class_grad == 'high':
        results = await api_client.get(UserEndpoints.get_high_classes)

    elif class_grad == 'preschool':
        results = await api_client.get(UserEndpoints.get_class_by_number, class_number=0)

    if not results:
        return False
    elif results is None:
        return None
    else:
        if class_grad != "preschool":
            result = results[0]
        else:
            result = results
        change = {
            'preschool': 'Дошкольная группа',
            'elementary': 'Начальные группы',
            'middle': 'Средние группы',
            'high': 'Старшие группы'
        }

        json_schedule = result['schedule']
        enter = '\n'
        text = (f"<b>{change[class_grad]}</b>\n\n"
                f"Цена в месяц без питания\n {result['price']} руб.\n"
                f"Цена в год без питания\n {int(result['price']) * 10} руб.\n\n"
                f"Расписание\n{enter.join(f'{key.capitalize()} : {value}' for key, value in json_schedule.items())}\n\n"
                f"Записаться на встречу\n{config.SCHOOL_CONTACT_NUMBER}"
                )
        kb = InlineKeyboardMarkup()
        kb.add(InlineKeyboardButton(text='Назад', callback_data=f'school_start'))

        return text, kb

