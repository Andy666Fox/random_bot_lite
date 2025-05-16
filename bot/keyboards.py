from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_main_keyboard():
    builder = ReplyKeyboardBuilder()
    builder.button(text="Найти канал")
    return builder.as_markup(resize_keyboard=True)