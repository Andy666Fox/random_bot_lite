from aiogram.types import CallbackQuery
from aiogram import F
from routers import basic_router
from database.methods import update_channel_rating
from utils.message_manager import message_manager
from utils.log_manager import log_manager


@basic_router.callback_query(F.data.startswith("rate:"))
async def handle_rating_callback(callback: CallbackQuery):
    await callback.message.edit_reply_markup(reply_markup=None)
    try:
        _, action, channelnick = callback.data.split(":", 2)
        print()
        score = 1 if action == "like" else -1
        success = await update_channel_rating(channelnick, score)
        if success:
            await callback.answer(message_manager.RATING_CALLBACK_SUCCESS)
            log_manager.log_user_event(
                callback.from_user.id,
                "channel_rating",
                data={f"User {callback.from_user.username} rated": channelnick},
            )
        else:
            await callback.answer(message_manager.RATING_CALLBACK_FAIL)
            log_manager.log_user_event(
                callback.from_user.id,
                "channel_rating_fail",
                data={f"User {callback.from_user.username} rate failed": channelnick},
            )
    except Exception as e:
        log_manager.log_error(e, context={"handle_rating_callback_func_error": e})