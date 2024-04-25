import asyncio
import logging
import os

from aiogram import Dispatcher, Bot, types
from aiogram.filters import Command
from dotenv import find_dotenv, load_dotenv

from src.news.keyboards import NewsKeyboards
from src.news.routers import router as news_router
from src.users.routers import router as user_router
from src.users.service import registration_user

load_dotenv(find_dotenv())

logging.basicConfig(level=logging.INFO)

API_TOKEN = os.getenv('API_TOKEN')

bot = Bot(token=API_TOKEN)

# Диспетчер

dp = Dispatcher()


@dp.message(Command("start"))
async def command_start(message: types.Message):
    user = await registration_user(message)
    if user is True:
        print('Новая регистрация')

    elif user is False:
        print('Зашел зарегистрированный пользователь!')
    return await NewsKeyboards.view_menu(message)


dp.include_routers(news_router)
dp.include_routers(user_router)


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())