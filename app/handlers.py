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
    if token != None:
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
        response_data = await api_res.authorization(data)

        try:
            await message.answer(f"*Ошибка* : {response_data['error']}", parse_mode="Markdown")
        except:
            await db_res.save_token(message.from_user.id, response_data['token'])
            await message.answer(f'{message.from_user.first_name}, авторизация завершена✌️', reply_markup=kb.main)
    except:
        await message.answer('❌Ошибка авторизации')
    finally:
        await state.clear()
        

#Получение студентов группы===========================================================================================


@router.message(lambda message: message.text == "Список студентов")
async def get_group_students(message: Message):
    token = await db_res.get_token(message.from_user.id)
    if token:
        response_data = await api_res.get_group_students(token)

        try:
            await message.answer(f"*Ошибка* : {response_data['error']}", parse_mode="Markdown")

        except:
            students = response_data["students"]
            msg = f"🧹Студенты группы: *{students[0]['group']}*\n\n"
            for student in students:
                msg += f"👨‍🎓 *@{student['username']}*, {student['full_name']}\n"
            await message.answer(msg, parse_mode="Markdown")
        
    else:
        await message.answer('Необходимо авторизоваться', reply_markup=kb.start)


#Получение списка дежурств===========================================================================================


@router.message(lambda message: message.text == "Список дежурств")
async def get_group_duties(message: Message):
    token = await db_res.get_token(message.from_user.id)
    if token:
        response_data = await api_res.get_group_duties(token)

        if "error" in response_data:
            await message.answer(f"*Ошибка* : {response_data['error']}", parse_mode="Markdown")
        elif "message" in response_data:
            await message.answer(f"*Сообщение* : {response_data['message']}", parse_mode="Markdown")

        else:
            msg = "🧹*Дежурства:*\n\n"
            duties = response_data["duties"]

            if duties == []:
                await message.answer("*🔎Дежурств не обнаружено*", parse_mode="Markdown")
            else:
                for duty in duties:
                    msg += f"👨‍🎓 *@{duty['attendant']['username']} {duty['attendant']['full_name']}* дежурил ⏰*{duty['date']}*\n"
                    await message.answer(msg, parse_mode="Markdown")
            
    else:
        await message.answer('Необходимо авторизоваться', reply_markup=kb.start)


#Получение количества дежурств===========================================================================================


@router.message(lambda message: message.text == "Количество дежурств")
async def get_group_duties_count(message: Message):
    token = await db_res.get_token(message.from_user.id)
    if token:
        response_data = await api_res.get_group_duties_count(token)

        if "error" in response_data:
            await message.answer(f"*Ошибка* : {response_data['error']}", parse_mode="Markdown")
        elif "message" in response_data:
            await message.answer(f"*Сообщение* : {response_data['message']}", parse_mode="Markdown")

        else:
            msg = "🧹*Количество дежурств:*\n\n"
            duties = response_data["duties"]

            if duties == []:
                await message.answer("*🔎Дежурств не обнаружено*", parse_mode="Markdown")
            else:
                for duty in duties:
                    msg += f"👨‍🎓 *@{duty['username']}* {duty['full_name']} *Количество дежурств*: *{duty['duties_count']}*\n"
                    await message.answer(msg, parse_mode="Markdown")


#Назначение дежурных===========================================================================================
    

@router.message(lambda message: message.text == "Назначить дежурных")
async def get_attendants(message: Message, state: FSMContext):
    token = await db_res.get_token(message.from_user.id)
    if token:
        data = await state.get_data()
        try: 
            pass_attendant = data['pass_attendant']
        except:
            pass_attendant = []

        response_data = await api_res.get_group_attendants(token, pass_attendant)

        if "error" in response_data:
            await message.answer(f"*Ошибка* : {response_data['error']}", parse_mode="Markdown")
        elif "message" in response_data:
            await message.answer(f"*Сообщение* : {response_data['message']}", parse_mode="Markdown")


        else:
            attendants = response_data["attendants"]
            await state.update_data(attendants=attendants)
            await state.update_data(pass_attendant=pass_attendant)
            try:
                await message.answer(f"👷🏿*{attendants[0]['full_name']}* 👷🏿*{attendants[1]['full_name']}*", reply_markup=kb.remap, parse_mode="Markdown")
            except:
                await message.edit_text(f'❗Куда гонишь?', reply_markup=kb.remap, parse_mode="Markdown")
    else:
        await message.answer('Необходимо авторизоваться', reply_markup=kb.cancel)
        await state.clear()
    

@router.callback_query(F.data == 'remapFirst')
async def remapFirst(callback:CallbackQuery, state: FSMContext):
    token = await db_res.get_token(callback.from_user.id)
    data = await state.get_data()
    firstAttendant = data['attendants'][0]['id']
    pass_attendant = data['pass_attendant']
    pass_attendant.append(firstAttendant)
    response_data = await api_res.get_group_attendants(token, pass_attendant)

    if "error" in response_data:
        await callback.message.answer(f"*Ошибка* : {response_data['error']}", parse_mode="Markdown")
    elif "message" in response_data:
        await callback.message.answer(f"*Сообщение* : {response_data['message']}", parse_mode="Markdown")

    else:
        attendants = response_data["attendants"]
        await state.update_data(attendants=attendants)
        await state.update_data(pass_attendant=pass_attendant)
        try:
            await callback.message.edit_text(f"👷🏿*{attendants[0]['full_name']}* 👷🏿*{attendants[1]['full_name']}*", reply_markup=kb.remap, parse_mode="Markdown")
        except:
            await callback.message.edit_text(f'❗Куда гонишь?', reply_markup=kb.cancel, parse_mode="Markdown")
    

@router.callback_query(F.data == 'remapSecond')
async def remapSecond(callback:CallbackQuery, state: FSMContext):
    token = await db_res.get_token(callback.from_user.id)
    data = await state.get_data()
    secondAttendant = data['attendants'][1]['id']
    pass_attendant = data['pass_attendant']
    pass_attendant.append(secondAttendant)
    response_data = await api_res.get_group_attendants(token, pass_attendant)

    if "error" in response_data:
        await callback.message.answer(f"*Ошибка* : {response_data['error']}", parse_mode="Markdown")
    elif "message" in response_data:
        await callback.message.answer(f"*Сообщение* : {response_data['message']}", parse_mode="Markdown")
    
    else:
        attendants = response_data["attendants"]
        await state.update_data(attendants=attendants)
        await state.update_data(pass_attendant=pass_attendant)
        try:
            await callback.message.edit_text(f"👷🏿*{attendants[0]['full_name']}* 👷🏿*{attendants[1]['full_name']}*", reply_markup=kb.remap, parse_mode="Markdown")
        except:
            await callback.message.edit_text(f'❗Куда гонишь?', reply_markup=kb.cancel, parse_mode="Markdown")


@router.callback_query(F.data == 'assign')
async def assign(callback:CallbackQuery, state: FSMContext):
    token = await db_res.get_token(callback.from_user.id)
    data = await state.get_data()
    response_data = attendants = data['attendants']

    await api_res.add_attendant_duties(token, attendants)

    if "error" in response_data:
        await callback.message.answer(f"*Ошибка* : {response_data['error']}", parse_mode="Markdown")
    elif "message" in response_data:
        await callback.message.answer(f"*Сообщение* : {response_data['message']}", parse_mode="Markdown")
    else:
        await callback.message.edit_text('✅Дежурные установлены')
        await state.clear()

@router.callback_query(F.data == 'cancel')
async def catalog(callback:CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text('✅Отменено')


@router.message(Command('help'))
async def get_help(message:Message):
    await message.answer('В разработке')

@router.message(Command('links'))
async def get_help(message:Message):
    await message.answer("👑Polina's Scrbbs links", reply_markup=kb.links)
