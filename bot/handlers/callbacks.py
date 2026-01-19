from aiogram import F
from aiogram.types import CallbackQuery
from database.methods import update_channel_rating
from utils.bot_answers import bot_answers
from utils.log_manager import bot_logger

from handlers import basic_router


@basic_router.callback_query(F.data.startswith("rate:"))
async def handle_rating_callback(callback: CallbackQuery):
    await callback.message.edit_reply_markup(reply_markup=None)
    try:
        _, action, channelnick = callback.data.split(":", 2)
        print()
        score = 1 if action == "like" else -1
        success = await update_channel_rating(channelnick, score)
        if success:
            await callback.answer(bot_answers.RATING_CALLBACK_SUCCESS)
            bot_logger.log_user_event(
                callback.from_user.id,
                "channel_rating",
                data={f"User {callback.from_user.username} rated": channelnick},
            )
        else:
            await callback.answer(bot_answers.RATING_CALLBACK_FAIL)
            bot_logger.log_user_event(
                callback.from_user.id,
                "channel_rating_fail",
                data={f"User {callback.from_user.username} rate failed": channelnick},
            )
    except Exception as e:
        bot_logger.log_error(e, context={"handle_rating_callback_func_error": e})
