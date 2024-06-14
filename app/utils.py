from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from .keyboards import start

async def handle_registration_response(message: Message, state: FSMContext, response_data):
    if "error" in response_data:
        await message.answer(f'❌*Ошибка:* {response_data["error"]}', parse_mode="Markdown", reply_markup=start)
    else:
        await message.answer('✅Регистрация прошла успешно!', reply_markup=start)
        await state.clear()