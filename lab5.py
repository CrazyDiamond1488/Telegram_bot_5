import logging
import os
import asyncio
from Hendlers import UserComand, UserMessange
from BD import  sql
from aiogram import Router
from app import TOKEN
# Библиотеки aiogram
from aiogram import Bot, Dispatcher, types, Router

async def main():
    logging.basicConfig(level=logging.INFO)
    token_bot = os.getenv('TOKEN_BOT')

    bot = Bot(token=TOKEN)
    dp = Dispatcher()

    dp.include_routers(
        UserComand.router, UserMessange.router
    )

    await dp.start_polling(bot)
if __name__ == '__main__':
    asyncio.run(main())



