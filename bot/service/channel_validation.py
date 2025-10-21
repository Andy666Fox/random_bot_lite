import requests

from service.log_manager import bot_logger


async def validate_channel(channelnick: str) -> bool:
    response = requests.get(f"https://t.me/{channelnick}")
    if response.status_code == 200:
        print("Request status 200, continue")
        if "preview channel" in response.text.lower():
            bot_logger.log_system_event("channel validation", data={channelnick: True})
            return True
    bot_logger.log_system_event("channel validation", data={channelnick: False})
    return False
