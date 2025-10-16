from aiogram.enums import ContentType

ANSWERS = ["Вот например:", "А как тебе этот:", "Что насчет этого:", "Ну вот собсна:", "Смари чо нашел:", "Вот что попалось:"]

START_MESSAGE = (
    "Добро пожаловать!\n"
    "Используйте кнопку ниже для получения канала\n"
    "Внимание! Используйте пожалуйста только кнопки\n"
    "В случае если не кнопка не появляется, отправьте '/start'"
)

# TODO Edit commands description
EXTRA_COMMANDS_DESCRIPTION = 'string'

ANSWER_TO_MEDIA = "Не нужно ничего мне отправлять\nЯ не Майкрософт"

ANSWER_TO_WRONG_TEXT = (
    "Чел, у меня памяти 2 килобайта, побойся бога.\nДавай только кнопками общаться плиз"
)

ANSWER_TO_FLOOD = "Отставить спам, погоди пару секунд"


# Запрещенные типы контента
BLOCKED_CONTENT_TYPES = [
    ContentType.PHOTO,
    ContentType.VIDEO,
    ContentType.DOCUMENT,
    ContentType.AUDIO,
    ContentType.VOICE,
    ContentType.VIDEO_NOTE,
    ContentType.STICKER,
    ContentType.ANIMATION,
]
