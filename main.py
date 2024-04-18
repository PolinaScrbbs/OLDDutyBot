import asyncio
from aiogram import Bot, Dispatcher

from config import BOT_TOKEN
from app.database.models import async_main
from app.handlers import router

async def main():
    await async_main()
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        print('Бот запущен')
        asyncio.run(main())
    except:
        print('Бот выключен')