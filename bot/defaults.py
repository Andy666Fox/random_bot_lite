from aiogram.enums import ContentType

ANSWERS = ["Вот например:", "А как тебе этот:", "Что насчет этого:", "Ну вот собсна:"]

START_MESSAGE = (
    "Добро пожаловать!\n"
    "Используйте кнопку ниже для получения канала\n"
    "Внимание! Используйте пожалуйста только кнопки"
)

MESSAGE_ANSWER = "Не нужно ничего мне отправлять\nЯ не Майкрософт"

DEFAULT_RESPONSE = (
    "Чел, у меня памяти 2 килобайта, побойся бога.\n"
    "Давай только кнопками общаться плиз"
)

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
