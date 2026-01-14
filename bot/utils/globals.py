from aiogram.enums import ContentType

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

STOP_WORDS = {
    # Русские
    'и', 'в', 'на', 'с', 'к', 'по', 'за', 'из', 'о', 'у', 'а', 'е', 'ё', 'й', 'я',
    'не', 'что', 'это', 'он', 'она', 'мы', 'вы', 'они', 'как', 'где', 'когда', 'почему',
    'так', 'же', 'бы', 'ли', 'ну', 'вот', 'же', 'для', 'от', 'до', 'же', 'или', 'но',
    'если', 'то', 'чтобы', 'который', 'этот', 'тот', 'весь', 'свой', 'мой', 'твой',
    # Английские
    'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with',
    'by', 'is', 'are', 'was', 'were', 'be', 'been', 'have', 'has', 'had', 'do', 'does',
    'did', 'will', 'would', 'could', 'should', 'may', 'might', 'can', 'this', 'that'
}
