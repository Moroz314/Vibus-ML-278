import asyncio

from aiogram import Bot, Dispatcher  
from aiogram.filters import CommandStart
from aiogram.types import Message
from config import TOKEN
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton


def keyboard_builder(width, *args):
    buttons = list(map(lambda x: InlineKeyboardButton(text=x, callback_data=x), args))
    kb_builder = InlineKeyboardBuilder()
    kb_builder.row(*buttons, width=width)
    return kb_builder.as_markup(resize_keyboard=True)


bot = Bot(token = TOKEN)
dp = Dispatcher()

async def main() :
    await dp.start_polling(bot)


@dp.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer('Приветствую тебя в боте для управления самого мощного семейство вирусов "VIBUS_ML_278" ! Ну а раз ты уже здесь то ты достоин !!!')
    keyboard = keyboard_builder(3, "Зараженные компьютеры", "Инструкция" , "Слова авторов")
    await message.answer(text="что делаем ?", reply_markup=keyboard)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')
