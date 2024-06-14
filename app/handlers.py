from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram.utils import markdown
from aiogram.fsm.context import FSMContext

import app.keyboards as kb
import app.states as st
import app.api.response as api_res
import app.database.response as db_res
from app.utils import handle_registration_response
from app.validators import RegistrationValidator

router = Router()

#Старт
@router.message(CommandStart())
async def cmd_start(message:Message):
    token = await db_res.get_token(message.from_user.id)
    if token:
        reply_markup = kb.main
    else:
        reply_markup = kb.start
    await message.answer(f'Привет👋\nВыбери пункт из меню🔍',
                        reply_markup=reply_markup)


#Регистрация============================================================================================================


@router.message(lambda message: message.text == "Регистрация")
async def get_full_name(message: Message, state: FSMContext):
    await state.update_data(username=message.from_user.username)
    await state.set_state(st.Registration.full_name)
    await message.answer('👨‍🎓Введите ФИО', reply_markup=kb.cancel)

@router.message(st.Registration.full_name)
async def get_password(message: Message, state: FSMContext):
    await state.update_data(full_name=message.text)
    await state.set_state(st.Registration.password)
    await message.answer('🔑Создайте пароль', reply_markup=kb.cancel)

@router.message(st.Registration.password)
async def get_confirm_password(message: Message, state: FSMContext):
    await state.update_data(password=message.text)
    await state.set_state(st.Registration.confirm_password)
    await message.answer('🔑Подтвердите пароль ', reply_markup=kb.cancel)

@router.message(st.Registration.confirm_password)
async def registration(message: Message, state: FSMContext):
    try:
        await state.update_data(confirm_password=message.text)
        data = await state.get_data()

        validator = RegistrationValidator(data["full_name"], data["password"], data["confirm_password"])
        error_message = await validator.validate()

        if error_message:
            await message.answer(f'❌*Ошибка:* {error_message}', parse_mode="Markdown", reply_markup=kb.start)
        else:
            response_data = await api_res.registration(data)
            await handle_registration_response(message, state, response_data)
    
    except Exception as e:
        await message.answer(f'❌*Ошибка:* {str(e)}', parse_mode="Markdown", reply_markup=kb.start)

    finally:
        await state.clear()


#Авторизация============================================================================================================


@router.message(lambda message: message.text == "Авторизация")
async def get_password(message: Message, state: FSMContext):
    await state.update_data(login=message.from_user.username)
    await state.set_state(st.Auth.password)
    await message.answer('🔑Введите пароль', reply_markup=kb.cancel)

@router.message(st.Auth.password)
async def authorazation(message: Message, state: FSMContext):
    await state.update_data(password=message.text)
    data = await state.get_data()

    try:
        token = await api_res.authorization(data)

        if token is None or "error" in token:
            await message.answer('❌Ошибка авторизации')
        else:
            await db_res.save_token(message.from_user.id, token)
            await message.answer(f'{message.from_user.first_name}, авторизация завершена✌️', reply_markup=kb.main)
    except:
        await message.answer('❌Ошибка авторизации')
    finally:
        await state.clear()
        

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
        print(duties)
        if error:
            await message.answer(error, reply_markup=kb.main)
        else:
            msg = "🧹*Дежурства:*\n\n"
            if duties != []:
                for duty in duties:
                    msg += f"👨‍🎓 *{duty['people']['full_name']}* дежурил ⏰*{duty['date']}*\n"
            else:
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
                await message.answer(f"👷🏿*{attendants[0]['full_name']}*{' ' * len(attendants[1]['full_name']) * 3}👷🏿*{attendants[1]['full_name']}*", reply_markup=kb.remap, parse_mode="Markdown")
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
            await callback.message.edit_text(f"👷🏿*{attendants[0]['full_name']}*{' ' * len(attendants[1]['full_name']) * 3}👷🏿*{attendants[1]['full_name']}*", reply_markup=kb.remap, parse_mode="Markdown")
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
            await callback.message.edit_text(f"👷🏿*{attendants[0]['full_name']}*{' ' * len(attendants[1]['full_name']) * 3}👷🏿*{attendants[1]['full_name']}*", reply_markup=kb.remap, parse_mode="Markdown")
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
    await message.answer('В разработке')

@router.message(Command('links'))
async def get_help(message:Message):
    await message.answer("👑Polina's Scrbbs links", reply_markup=kb.links)
