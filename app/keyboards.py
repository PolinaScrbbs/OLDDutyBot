from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton, WebAppInfo,
                           InlineKeyboardMarkup, InlineKeyboardButton)

from aiogram.utils.keyboard import KeyboardBuilder, ReplyKeyboardBuilder, InlineKeyboardBuilder

start = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Авторизация')],
    [KeyboardButton(text='Создатель', web_app=WebAppInfo(url='https://github.com/PolinaScrbbs'))]
],
                        resize_keyboard=True,
                        input_field_placeholder='Выберите пункт меню')

cancel = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='❌Отмена', callback_data='cancel')]
])

settings = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Создатель', url='https://github.com/PolinaScrbbs')]
])

links = ['Первая', 'Вторая', 'Третья']

async def inline_links():
    keyboard = InlineKeyboardBuilder()
    for link in links:
        keyboard.add(InlineKeyboardButton(text=link, url='https://github.com/PolinaScrbbs'))
    return keyboard.adjust(2).as_markup() #adjust(2) По 2 кнопки в ряду
    