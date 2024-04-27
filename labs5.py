# Системные библиотеки
import logging
import os
import asyncio
from Hendlers import UserComand, UserMessange
from BD import  sql
from aiogram import Router
from app import TOKEN

# Библиотеки aiogram
from aiogram import Bot, Dispatcher, types, Router
from aiogram.types import  BotCommand, BotCommandScopeDefault

async def set_default_commands(bot: Bot):
    return await bot.set_my_commands(
        commands=[
            BotCommand(command='start', description='Начать'),
            BotCommand(command='get_currencies', description='Просмотр валют'),
            BotCommand(command='convert', description='Конвертировать'),
        ],
        scope=BotCommandScopeDefault(),
    )

async def main():
    logging.basicConfig(level=logging.INFO)
    token_bot = os.getenv('TOKEN_BOT')

    bot = Bot(token=TOKEN)
    dp = Dispatcher()

    dp.include_routers(
        UserComand.router, UserMessange.router
    )
    await set_default_commands(bot)

    await dp.start_polling(bot)
if __name__ == '__main__':
    asyncio.run(main())
