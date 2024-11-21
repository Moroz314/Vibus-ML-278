from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton


def keyboard_builder(width, *args):
    buttons = list(map(lambda x: InlineKeyboardButton(text=x, callback_data=x), args))
    kb_builder = InlineKeyboardBuilder()
    kb_builder.row(*buttons, width=width)
    return kb_builder.as_markup(resize_keyboard=True)