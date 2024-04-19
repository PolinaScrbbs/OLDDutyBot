from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton, WebAppInfo,
                           InlineKeyboardMarkup, InlineKeyboardButton)

from aiogram.utils.keyboard import KeyboardBuilder, ReplyKeyboardBuilder, InlineKeyboardBuilder

start = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Авторизация')],
    [KeyboardButton(text='Создатель', web_app=WebAppInfo(url='https://github.com/PolinaScrbbs'))]
],
                        resize_keyboard=True,
                        input_field_placeholder='Выберите пункт меню')

main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Назначить дежурных'), KeyboardButton(text='Получить количество дежурств')],
    [KeyboardButton(text='Получить список дежурств')],
    [KeyboardButton(text='Создатель', web_app=WebAppInfo(url='https://github.com/PolinaScrbbs'))]
],
                        resize_keyboard=True,
                        input_field_placeholder='Выберите пункт меню')

remap = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='🔄', callback_data='remapFirst'), InlineKeyboardButton(text='🔄', callback_data='remapSecond')],
    [InlineKeyboardButton(text='✅Назначить', callback_data='assign')], 
    [InlineKeyboardButton(text='❌Отмена', callback_data='cancel')]
], 
                        row_width=1)

cancel = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='❌', callback_data='cancel')]
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
    