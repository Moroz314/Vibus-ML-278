import asyncio

from aiogram import Bot, Dispatcher  
from aiogram.filters import CommandStart
from aiogram.types import Message


bot = Bot(token = '7745882842:AAEXRdIXFN4yzIriT5Eo0bNgG2GvkXnGi74')
dp = Dispatcher()

async def main() :
    await dp.start_polling(bot)


@dp.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer('Привет')


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')
