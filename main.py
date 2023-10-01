import asyncio
from aiogram import Dispatcher, Bot
from app.handlers import router

async def main():
    bot = Bot(token='6417911828:AAHLlrjFJx1jvM2lDEblisLz3ijk3N2szr8')
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except Exception as e:
        print(f'Error: {e}')
