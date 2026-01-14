import os
import requests
from utils.log_manager import log_manager


class Validation:
    def __init__(self):
        pass

    async def is_admin(self, user_id: int) -> bool:
        return bool(1 - bool(user_id ^ int(os.getenv("ADMIN_ID"))))

    async def validate_channel(self, channelnick: str) -> bool:
        response = requests.get(f"https://t.me/{channelnick}")
        if response.status_code == 200:
            print("Request status 200, continue")
            if "preview channel" in response.text.lower():
                log_manager.log_system_event("channel validation", data={channelnick: True})
                return True
        log_manager.log_system_event("channel validation", data={channelnick: False})
        return False


validation_manager = Validation()
