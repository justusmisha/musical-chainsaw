from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, InputFile, InputMedia

from Bot.app.api.endpoints import UserEndpoints
from Bot.app.data import config
from Bot.app.keyboards.user.classes import start_classes_menu, get_all_classes_kb
from Bot.app.keyboards.user.general import kb_menu_back
from Bot.app.keyboards.user.school import school_about_kb, school_clubs, schedule_choice
from Bot.app.utils.photos import load_school_photos, get_schedule_photo
from Bot.app.utils.school import get_class_info, get_grad_info
from Bot.loader import dp, api_client
from logger import logger


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
        text = (f"<b>{teacher['fio']}</b>\n"
                f"Предмет: {teacher['subject']}\n"
                )
        with open(teacher['file_path'], 'rb') as file:
            if file:
                await call.message.answer_document(document=file, caption=text)
            else:
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
            return
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


@dp.callback_query_handler(text='school_food', state='*')
async def about_school_food(call: CallbackQuery):
    text = (f"{config.SCHOOL_FOOD_INFO}\n\n"
            f"Дополнительная плата в месяц: {config.SCHOOL_FOOD_PRICE}\n"
            f"Дополнительная плата в год: {config.SCHOOL_FOOD_PRICE * 10}")

    await call.message.edit_text(text=text,
                                 reply_markup=kb_menu_back)


from aiogram.types import InputFile, InlineKeyboardMarkup, InlineKeyboardButton


@dp.callback_query_handler(lambda c: c.data.startswith('teachers_class_'), state='*')
async def teachers_for_class_handle(call: CallbackQuery):
    class_number = call.data.split('teachers_class_')[-1]

    results = await api_client.get(UserEndpoints.get_teacher_by_class, class_number=class_number)

    if results is False:
        await call.message.answer(text='❌ Возникла ошибка с получением преподавателей для группы')
        return
    elif results is None:
        await call.message.answer(text='❌ Нет преподавателей или они еще не были добавлены')
        return

    for teacher in results:
        text = f"{teacher['fio']}\nГруппа: {class_number}\nПредмет: {teacher['subject']}\n"

        file_path = teacher['file_path']
        if file_path:
            document = InputFile(file_path)
            await call.message.answer_document(document=document, caption=text)
        else:
            await call.message.answer(text=text)


@dp.callback_query_handler(text='about_schedule', state='*')
async def schedule_handler(call: CallbackQuery):
    kb = await schedule_choice()
    await call.message.edit_text(text='Выберите день недели', reply_markup=kb)


@dp.callback_query_handler(lambda c: c.data.startswith('about_schedule_'), state='*')
async def schedule_day_handler(call: CallbackQuery):
    day = call.data.split('about_schedule_')[-1]
    photo = await get_schedule_photo(day)
    if not photo:
        await call.message.answer(text='❌ Возникла проблема с загрузкой расписания')
        return
    days_trans = {
        'monday': 'Понедельник',
        'tuesday': 'Вторник',
        'wednesday': 'Среда',
        'thursday': 'Четверг',
        'friday': 'Пятница',
    }
    await call.message.answer_photo(photo=photo, caption=f'Расписание на {days_trans[day]}',
                                    reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton(text='◀️ Назад', callback_data='school_start_answer')))


@dp.callback_query_handler(text='about_photos', state='*')
async def send_school_photos(call: CallbackQuery):
    media_group = await load_school_photos()

    if media_group:
        try:
            await call.message.answer_media_group(media=media_group)

            await call.message.answer(text=f"Фотографии были загружены",
                                      reply_markup=InlineKeyboardMarkup().add(
                                          InlineKeyboardButton(text='◀️ Назад',
                                                               callback_data=f'school_start')))
        except Exception as e:
            logger.error(f"Error sending media group: {e}")
            await call.message.answer(text='Произошла ошибка при отправке фотографий.')
    else:
        await call.message.answer(text='Не удалось загрузить фотографии.')