from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart, Command
from aiogram import Router
from aiogram.types import Message
#Импорт кнопок
from KeyBoards.KeyBoard import mains

router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message):
    user = message.from_user
    username = user.username if user.username else "Не указано"
    await message.answer(f'Привет!, {username}', reply_markup=mains)
