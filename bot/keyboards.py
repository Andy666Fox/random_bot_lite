from aiogram.utils.keyboard import ReplyKeyboardBuilder


def get_main_keyboard():
    builder = ReplyKeyboardBuilder()
    builder.button(text="Найти канал")
    return builder.as_markup(resize_keyboard=True)
