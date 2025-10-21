import os


def is_admin(user_id: int) -> bool:
    return bool(1 - bool(user_id ^ int(os.getenv("ADMIN_ID"))))
