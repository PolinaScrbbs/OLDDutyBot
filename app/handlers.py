from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

import app.keyboards as kb
import app.states as st
import app.api.response as api_res
import app.database.response as db_res

router = Router()

#Старт
@router.message(CommandStart())
async def cmd_start(message:Message):
    await message.answer(f'Привет {message.from_user.first_name} {message.from_user.last_name}\nВыбери пункт из меню💤💤💤',
                        reply_markup=kb.start)


#Авторизация============================================================================================================


@router.message(lambda message: message.text == "Авторизация")
async def get_login(message: Message, state: FSMContext):
    await state.set_state(st.Auth.login) #Поменяли состояние на ожидание логина
    await message.answer('Введите логин', reply_markup=kb.cancel)

@router.message(st.Auth.login)
async def get_password(message: Message, state: FSMContext):
    await state.update_data(login=message.text) #Сохранили логин
    await state.set_state(st.Auth.password) #Поменяли состояние на ожидание пароля
    await message.answer('Введите пароль', reply_markup=kb.cancel)

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
