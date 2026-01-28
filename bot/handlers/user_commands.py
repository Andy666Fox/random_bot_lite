from aiogram import F, Router, types
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter

from database.methods import insert_suggested_channel, insert_user, update_channel_rating
from keyboards.builder import get_main_keyboard, get_suggest_cancel_keyboard
from middlewares.middlewares import CooldownMW
from utils.log_manager import log_manager
from utils.message_manager import message_manager
from utils.validation_manager import validation_manager
from utils.globals import SuggestStates

user_commands_router = Router()
user_commands_router.message.middleware(CooldownMW())


@user_commands_router.callback_query(F.data.startswith("rate:"))
async def handle_rating_callback(callback: types.CallbackQuery):
    await callback.message.edit_reply_markup(reply_markup=None)
    try:
        _, action, channelnick = callback.data.split(":", 2)
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

@user_commands_router.message(Command("start"))
async def send_welcome(message: types.Message):
    uid = message.from_user.id
    first_name = message.from_user.first_name if message.from_user.first_name else ""
    last_name = " " + message.from_user.last_name if message.from_user.last_name else ""
    nickname = first_name + last_name
    status = await insert_user(uid, nickname)
    if status:
        msg = message_manager.NEW_USER_HELLO.format(nickname) + message_manager.START_INFO
    else:
        msg = message_manager.OLD_USER_HELLO.format(nickname) + message_manager.START_INFO
    log_manager.log_user_event(uid, "start", data={"Bot started by user": nickname})
    await message.answer(msg, reply_markup=get_main_keyboard())


@user_commands_router.message(Command("extra"))
async def send_extra_commands(message: types.Message):
    log_manager.log_user_event(
        message.from_user.id,
        "extra",
        data={"Looked for extra commands": message.from_user.id},
    )
    await message.answer(message_manager.EXTRA_COMMANDS_DESCRIPTION,
                        reply_markup=get_main_keyboard())

async def _prompt_for_next_channel(message: types.Message, entry=True):
    if entry:
        await message.answer(
            message_manager.FIRST_ASK_FOR_CHANNEL_LINK,
            reply_markup=get_suggest_cancel_keyboard()
        )
    else:
        await message.answer(
            message_manager.LOOP_ASK_FOR_CHANNEL_LINK,
            reply_markup=get_suggest_cancel_keyboard()
        )

@user_commands_router.message(Command("suggest"))
async def suggest_channel_start(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state == SuggestStates.waiting_for_channel:
        await message.answer(message_manager.SUGGEST_ALREADY_ACTIVE)
        return
    
    await state.set_state(SuggestStates.waiting_for_channel)
    await _prompt_for_next_channel(message)

    log_manager.log_system_event(
        "suggest_mode_activated",
        data={"username": message.from_user.username}
    )

@user_commands_router.message(StateFilter(SuggestStates.waiting_for_channel), F.text == "Отмена")
async def suggest_cancel(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer(
        message_manager.SUGGEST_CANCELLED,
        reply_markup=get_main_keyboard()
    )

    log_manager.log_system_event(
        "suggest_mode_deactivated",
        data={"reason": "user_cancelled",
              "username": message.from_user.username}
    )

@user_commands_router.message(StateFilter(SuggestStates.waiting_for_channel))
async def suggest_channel_process(message: types.Message, state: FSMContext):
    linktext = message.text.strip()

    if linktext.startswith('/'):
        if linktext.startswith('/suggest'):
            await message.answer(message_manager.SUGGEST_ALREADY_ACTIVE)
            return

    if "t.me" in linktext:
        linktext = linktext.split("/")[-1]
    elif linktext.startswith("@"):
        linktext = linktext[1:]

    if await validation_manager.validate_channel(linktext):
        status = await insert_suggested_channel(linktext)
        match status[1]:
            case "created":
                response = message_manager.SUGGEST_SUCCESS
            case "exists":
                response = message_manager.SUGGEST_EXISTS
            case "error":
                response = message_manager.SUGGEST_FAIL
    else:
        status = ("failed", "invalid")
        response = message_manager.SUGGEST_FAIL

    log_manager.log_user_event(
        message.from_user.id,
        "suggest_attempt",
        data={"input_link": message.text.strip(),
              "extracted_nick": linktext,
              "status": status,
              "username": message.from_user.username},
    )

    await message.answer(response)
    await _prompt_for_next_channel(message, entry=False)