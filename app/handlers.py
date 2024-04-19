from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram.utils import markdown
from aiogram.fsm.context import FSMContext

import app.keyboards as kb
import app.states as st
import app.api.response as api_res
import app.database.response as db_res

router = Router()

#Старт
@router.message(CommandStart())
async def cmd_start(message:Message):
    token = await db_res.get_token(message.from_user.id)
    if token:
        reply_markup = kb.main
    else:
        reply_markup = kb.start
    await message.answer(f'Привет {message.from_user.first_name} {message.from_user.last_name}\nВыбери пункт из меню💤💤💤',
                        reply_markup=reply_markup)


#Авторизация============================================================================================================


@router.message(lambda message: message.text == "Авторизация")
async def get_login(message: Message, state: FSMContext):
    await state.set_state(st.Auth.login) #Поменяли состояние на ожидание логина
    await message.answer('🆔Введите логин', reply_markup=kb.cancel)

@router.message(st.Auth.login)
async def get_password(message: Message, state: FSMContext):
    await state.update_data(login=message.text) #Сохранили логин
    await state.set_state(st.Auth.password) #Поменяли состояние на ожидание пароля
    await message.answer('🔑Введите пароль', reply_markup=kb.cancel)

@router.message(st.Auth.password)
async def reg(message: Message, state: FSMContext):
    await state.update_data(password=message.text) #Сохранили пароль
    data = await state.get_data() #Получили информацию
    token, error = api_res.authorization(data['login'], data['password'])
    if error:
        await message.answer(error)
        await message.answer('Введите логин', reply_markup=kb.cancel)
        await state.set_state(st.Auth.login) #Поменяли состояние на ожидание логина
    else:
        await db_res.save_token(message.from_user.id, token)
        await message.answer(f'{message.from_user.first_name}, авторизация завершена')
        await state.clear() #Очищение состояний


#Получение людей===========================================================================================


@router.message(lambda message: message.text == "Получить количество дежурств")
async def get_people(message: Message):
    token = await db_res.get_token(message.from_user.id)
    if token:
        people, error = api_res.get_people(token)
        if error:
            await message.answer(error, reply_markup=kb.main)
        else:
            msg = "🧹*Количество дежурств:*\n\n"
            for person in people:
                msg += f"👨‍🎓 *{person['full_name']}* Количество дежурств: *{person['duties_count']}*\n"
            await message.answer(msg, parse_mode="Markdown")
    else:
        await message.answer('Необходимо авторизоваться', reply_markup=kb.start)


#Получение списка дежурств===========================================================================================


@router.message(lambda message: message.text == "Получить список дежурств")
async def get_duties(message: Message):
    token = await db_res.get_token(message.from_user.id)
    if token:
        duties, error = api_res.get_duties(token)
        if error:
            await message.answer(error, reply_markup=kb.main)
        else:
            msg = "🧹*Дежурства:*\n\n"
            if len(duties) > 1:
                for duty in duties:
                    msg += f"👨‍🎓 *{duty['people']['full_name']}* дежурил ⏰*{duty['date']}*\n"
            msg = "*🔎Дежурств не обнаружено*"
            await message.answer(msg, parse_mode="Markdown")
    else:
        await message.answer('Необходимо авторизоваться', reply_markup=kb.start)


#Назначение дежурных===========================================================================================
    

@router.message(lambda message: message.text == "Назначить дежурных")
async def get_attendants(message: Message, state: FSMContext):
    token = await db_res.get_token(message.from_user.id)
    if token:
        data = await state.get_data()
        try: 
            pass_people = data['pass_people']
        except:
            pass_people = []
        attendants, error = api_res.get_attendants(token, pass_people)
        if error:
            await message.edit_text(error, reply_markup=kb.main)
        else:
            await state.update_data(attendants=attendants)
            await state.update_data(pass_people=pass_people)
            try:
                await message.answer(f'👷🏿*{attendants[0]['full_name']}*{" "*len(attendants[1]['full_name'])*3}👷🏿*{attendants[1]['full_name']}*', reply_markup=kb.remap, parse_mode="Markdown")
            except:
                await message.edit_text(f'❗Куда гонишь?', reply_markup=kb.remap, parse_mode="Markdown")
    else:
        await message.answer('Необходимо авторизоваться', reply_markup=kb.cancel)
        await state.clear() #Очищение состояний
    

@router.callback_query(F.data == 'remapFirst')
async def remapFirst(callback:CallbackQuery, state: FSMContext):
    token = await db_res.get_token(callback.from_user.id)
    data = await state.get_data()
    firstAttendant = data['attendants'][0]['id']
    pass_people = data['pass_people']
    pass_people.append(firstAttendant)
    attendants, error = api_res.get_attendants(token, pass_people)
    if error:
        await callback.message.edit_text(error, reply_markup=kb.main)
    else:
        await state.update_data(attendants=attendants)
        await state.update_data(pass_people=pass_people)
        try:
            await callback.message.edit_text(f'👷🏿*{attendants[0]['full_name']}*{" "*len(attendants[1]['full_name'])*3}👷🏿*{attendants[1]['full_name']}*', reply_markup=kb.remap, parse_mode="Markdown")
        except:
            await callback.message.edit_text(f'❗Куда гонишь?', reply_markup=kb.cancel, parse_mode="Markdown")
    

@router.callback_query(F.data == 'remapSecond')
async def remapSecond(callback:CallbackQuery, state: FSMContext):
    token = await db_res.get_token(callback.from_user.id)
    data = await state.get_data()
    secondAttendant = data['attendants'][1]['id']
    pass_people = data['pass_people']
    pass_people.append(secondAttendant)
    attendants, error = api_res.get_attendants(token, pass_people)
    if error:
        await callback.message.edit_text(error, reply_markup=kb.main)
    else:
        await state.update_data(attendants=attendants)
        await state.update_data(pass_people=pass_people)
        try:
            await callback.message.edit_text(f'👷🏿*{attendants[0]['full_name']}*{" "*len(attendants[1]['full_name'])*3}👷🏿*{attendants[1]['full_name']}*', reply_markup=kb.remap, parse_mode="Markdown")
        except:
            await callback.message.edit_text(f'❗Куда гонишь?', reply_markup=kb.cancel, parse_mode="Markdown")


@router.callback_query(F.data == 'assign')
async def assign(callback:CallbackQuery, state: FSMContext):
    token = await db_res.get_token(callback.from_user.id)
    data = await state.get_data()
    attendants = data['attendants']
    api_res.post_duties(token, attendants)
    await callback.message.edit_text('✅Дежурные установлены')
    await state.clear() #Очищение состояний

@router.callback_query(F.data == 'cancel')
async def catalog(callback:CallbackQuery, state: FSMContext):
    await state.clear() #Очищение состояний
    await callback.message.edit_text('✅Отменено')


@router.message(Command('help'))
async def get_help(message:Message):
    await message.answer('Это команда /help')


@router.message(F.text == 'Как дела?')
async def how_are_you(message:Message):
    await message.answer('Хорошо')


@router.message(F.photo)
async def get_photo_id(message:Message):
    await message.answer(f'ID фото: {message.photo[-1].file_id}')


@router.message(Command('get_photo'))
async def get_photo(message:Message):
    await message.answer_photo(photo='AgACAgIAAxkBAAPAZiEzU-ZmNo4lPSA3lOUxV3IQsGkAAtXXMRsUXwhJWuZtoLaC9hcBAAMCAAN5AAM0BA',
                        caption='Ваше фото')
    
@router.callback_query(F.data == 'catalog')
async def catalog(callback:CallbackQuery):
    await callback.answer('Вы выбрали каталог', show_alert=True) #show_alert=True Показывает целое сообщение
    await callback.message.edit_text('Каталог', reply_markup=await kb.inline_links()) #Заменяем старые кнопки на новые
