from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton, WebAppInfo,
                           InlineKeyboardMarkup, InlineKeyboardButton)

from aiogram.utils.keyboard import KeyboardBuilder, ReplyKeyboardBuilder, InlineKeyboardBuilder

start = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Авторизация'), KeyboardButton(text='Регистрация')],
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

links = InlineKeyboardMarkup(inline_keyboard=[
    [   
        InlineKeyboardButton(text='📝Документация', url='https://github.com/PolinaScrbbs/DutyBot/blob/main/README.md'),
        InlineKeyboardButton(text='🖥️GitHub', url='https://github.com/PolinaScrbbs'),
        InlineKeyboardButton(text='💬Telegram', url='https://t.me/PolinaScrbbs')
    ]
]
                             )

settings = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Создатель', url='https://github.com/PolinaScrbbs')]
])
    