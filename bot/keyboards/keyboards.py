from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

# basic keyboard
def get_main_keyboard():
    builder = ReplyKeyboardBuilder()
    builder.button(text="Найти канал")
    return builder.as_markup(resize_keyboard=True)

def get_channel_rating_inline_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text='👍')
    builder.button(text='👎')
    return builder.as_markup()
