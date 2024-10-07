from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

from Bot.app.api.endpoints import UserEndpoints
from Bot.app.data import config
from Bot.app.keyboards.user.classes import start_classes_menu, get_all_classes_kb
from Bot.app.keyboards.user.school import school_about_kb, school_clubs
from Bot.app.utils.school import get_class_info, get_grad_info
from Bot.loader import dp, api_client


@dp.callback_query_handler(text='school_about', state='*')
async def school_about_handler(call: CallbackQuery):
    kb = await school_about_kb()
    await call.message.edit_text(text=f'Информация о школе \n'
                                      f'{config.SCHOOL_INFO}',
                                 reply_markup=kb)


@dp.callback_query_handler(text='about_teachers', state='*')
async def about_teachers_handler(call: CallbackQuery):
    teachers = await api_client.get(UserEndpoints.get_all_teachers)
    if not teachers:
        await call.message.answer(text='❌ Возникла ошибка с получением учителей')
        return
    elif teachers is None:
        await call.message.answer(text='❌ Учителей пока что нет или не были добавлены')
        return

    for teacher in teachers:
        text = (f"ФИО: {teacher['name']} {teacher['surname']}\n\n"
                f"Возраст: {teacher['age']}\n"
                f"Опыт работы с детьми: {teacher['experience']}\n"
                f"Об учителе: {teacher['description']}\n"
                )
        await call.message.answer(text=text)




@dp.callback_query_handler(lambda c: c.data.startswith('school_classes_'), state='*')
async def classes_handler(call: CallbackQuery):
    param = call.data.split('school_classes_')[-1]
    if param == 'info':
        price = False
        info = True
    else:
        price = True
        info = False

    kb = await start_classes_menu(price=price, info=info)
    await call.message.edit_text(text=config.CLASSES_INFO,
                                 reply_markup=kb)


@dp.callback_query_handler(lambda c: c.data.startswith('class_grad_'), state='*')
async def classes_handler(call: CallbackQuery):
    class_grad = call.data.split('_')[-2]
    method = call.data.split('_')[-1]
    if method == 'info':
        text = ''
        if class_grad == 'preschool':
            class_data = await get_class_info(class_number=0)
            if not class_data:
                await call.message.answer(text='❌ Возникла проблема с загрузкой класса(ов)')
                return
            text, kb = class_data
            await call.message.edit_text(text=text,
                                         reply_markup=kb)
        elif class_grad == 'elementary':
            text = 'Информация о младшей школе'
        elif class_grad == 'middle':
            text = 'Информация о средней школе'
        elif class_grad == 'high':
            text = 'Информация о старшей школе'

        kb = await get_all_classes_kb(class_grad)
        if not kb:
            await call.message.answer(text='❌ Возникла ошибка с загрузкой классов')
        elif kb is None:
            await call.message.answer(text='❌ Классов выбраной категории пока что не существует')

        await call.message.edit_text(text=text, reply_markup=kb)
    elif method == 'price':
        class_data = await get_grad_info(class_grad)
        if not class_data:
            await call.message.answer(text='❌ Возникла ошибка с загрузкой цен категории')
            return
        text, kb = class_data
        await call.message.edit_text(text=text, reply_markup=kb)


@dp.callback_query_handler(lambda c: c.data.startswith('class_number_'), state='*')
async def handle_class_number(call: CallbackQuery):
    class_number = call.data.split('class_number_')[-1]
    if isinstance(class_number, int):
        class_number = int(call.data.split('class_number_')[-1])
    class_data = await get_class_info(class_number=class_number)
    if not class_data:
        await call.message.answer(text='❌ Возникла проблема с загрузкой класса(ов)')
        return
    text, kb = class_data
    await call.message.edit_text(text=text,
                                 reply_markup=kb)


@dp.callback_query_handler(text='school_prices', state='*')
async def handle_class_number(call: CallbackQuery):
    class_number = call.data.split('class_number_')[-1]
    if isinstance(class_number, int):
        class_number = int(call.data.split('class_number_')[-1])
    class_data = await get_class_info(class_number=class_number)
    if not class_data:
        await call.message.answer(text='❌ Возникла проблема с загрузкой класса(ов)')
        return
    text, kb = class_data
    await call.message.edit_text(text=text,
                                 reply_markup=kb)