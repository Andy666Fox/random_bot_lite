from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder


# basic keyboard
def get_main_keyboard():
    builder = ReplyKeyboardBuilder()
    builder.button(text="Найти канал")
    return builder.as_markup(resize_keyboard=True)


def get_channel_rating_inline_keyboard(channelnick: str):
    builder = InlineKeyboardBuilder()
    builder.button(text="👍", callback_data=f"rate:like:{channelnick}")
    builder.button(text="👎", callback_data=f"rate:dislike:{channelnick}")
    builder.adjust(2)
    return builder.as_markup()

def get_suggest_cancel_keyboard():
    builder = ReplyKeyboardBuilder()
    builder.button(text="Отмена")
    return builder.as_markup(resize_keyboard=True, one_time_keyboard=False)
