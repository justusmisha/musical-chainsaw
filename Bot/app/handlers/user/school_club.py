from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto

from Bot.app.api.endpoints import UserEndpoints
from Bot.app.bot_loader import bot
from Bot.app.data.config import  ERROR_MESSAGE
from Bot.app.keyboards.user.general import kb_menu_back
from Bot.app.keyboards.user.school import school_clubs, one_activ
from Bot.app.utils.activiy import activ_by_name
from Bot.app.utils.photos import load_photos
from Bot.loader import dp, api_client
from logger import logger


@dp.callback_query_handler(text='school_clubs')
async def school_activs_handler(call: CallbackQuery):
    kb = await school_clubs()
    if kb is None:
        await call.message.edit_text(text='Кружков пока что нет',
                                 reply_markup=kb_menu_back)
    elif not kb:
        await call.message.answer(text='Возникла ошибка с получением кружков\n'
                                       f'{ERROR_MESSAGE}')
    else:
        await call.message.edit_text(text='Нажмите на занятие чтоб узнать о нем подробнее',
                                     reply_markup=kb)


@dp.callback_query_handler(lambda c: c.data.startswith('school_club_'), state='*')
async def activ_name_handler(call: CallbackQuery, state: FSMContext):
    activ_name = call.data.split('school_club_')[-1]
    result = await activ_by_name(activ_name)
    if not result:
        await call.message.answer(text=f'Возникла ошибка с получением кружка под названием {activ_name}\n'
                                       f'{ERROR_MESSAGE}')
    elif result is None:
        await call.message.edit_text(text='Кружков с таким названием нет',
                                     reply_markup=InlineKeyboardMarkup().add(
                                         InlineKeyboardButton(text='◀️ Назад', callback_data='school_start')))
    else:
        kb = await one_activ(result['name'])
        await call.message.edit_text(text=f"<b>{result['name']}</b>", reply_markup=kb)


@dp.callback_query_handler(lambda c: c.data.startswith('school_activ_schedule_'), state='*')
async def activ_schedule_handler(call: CallbackQuery, state: FSMContext):
    activ_name = call.data.split("school_activ_schedule_")[-1]
    result = await activ_by_name(activ_name)
    if not result:
        await call.message.answer(text=f'Возникла ошибка с получением расписания кружка под названием {activ_name}\n'
                                       f'{ERROR_MESSAGE}')
        return
    json_schedule = result['schedule']
    enter = '\n'
    text = (f"<i>Актуальное расписание для кружка</i> <b>{result['name']}</b>\n\n"
            f"{enter.join(f'{key} : {value}' for key, value in json_schedule.items())}")

    await call.message.edit_text(text=text,
                                 reply_markup=
                                 InlineKeyboardMarkup().add(
                                     InlineKeyboardButton(text='◀️ Назад', callback_data=f'school_club_{activ_name}')))


@dp.callback_query_handler(lambda c: c.data.startswith('school_activ_price_'), state='*')
async def activ_schedule_handler(call: CallbackQuery, state: FSMContext):
    activ_name = call.data.split("school_activ_price_")[-1]
    result = await activ_by_name(activ_name)
    if not result:
        await call.message.answer(text=f'Возникла ошибка с получением расписания кружка под названием {activ_name}\n'
                                       f'{ERROR_MESSAGE}')
        return
    prices = result['prices']
    text = (f"<b>Актуальные цены на <i>{activ_name}</i></b>\n\n"
            f"Одноразовое занятие: {prices['one']} руб.\n"
            f"Четырехразовое занятие: {prices['four']} руб.\n"
            f"Восемь занятий: {prices['eight']} руб.\n"
            f"Абонимент на месяц: {prices['month']} руб.\n")
    await call.message.edit_text(text=text, reply_markup=InlineKeyboardMarkup().add(
                                     InlineKeyboardButton(text='◀️ Назад', callback_data=f'school_club_{activ_name}')))


@dp.callback_query_handler(lambda c: c.data.startswith('school_activ_photos_'), state='*')
async def activ_photo_handler(call: CallbackQuery):
    activ_name = call.data.split("school_activ_photos_")[-1]
    result = await activ_by_name(activ_name)
    if not result:
        await call.message.answer(text=f'Возникла ошибка с получением контактов кружка под названием {activ_name}\n'
                                       f'{ERROR_MESSAGE}')
        return

    media_group = await load_photos()

    if media_group:
        try:
            await call.message.answer_media_group(media=media_group)

            await call.message.answer(text=f"Фотографии с кружка <b>{activ_name}</b> были загружены", reply_markup=InlineKeyboardMarkup().add(
                InlineKeyboardButton(text='◀️ Назад', callback_data=f'school_club_{activ_name}')))
        except Exception as e:
            logger.error(f"Error sending media group: {e}")
            await call.message.answer(text='Произошла ошибка при отправке фотографий.')
    else:
        await call.message.answer(text='Не удалось загрузить фотографии.')


@dp.callback_query_handler(lambda c: c.data.startswith('school_activ_contact_'), state='*')
async def activ_contact_handler(call: CallbackQuery):
    activ_name = call.data.split("school_activ_contact_")[-1]
    result = await activ_by_name(activ_name)
    if not result:
        await call.message.answer(text=f'Возникла ошибка с получением контактов кружка под названием {activ_name}\n'
                                       f'{ERROR_MESSAGE}')
        return

    text = (f"<b>Запись на кружок <i>{result['name']}</i></b> по телефону\n\n"
            f"{result['contact_number']}")
    await call.message.edit_text(text=text, reply_markup=InlineKeyboardMarkup().add(
        InlineKeyboardButton(text='◀️ Назад', callback_data=f'school_club_{activ_name}')))