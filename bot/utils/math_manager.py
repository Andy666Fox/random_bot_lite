from utils.log_manager import log_manager
import requests
from bs4 import BeautifulSoup

class MathManager:
    def __init__(self):
        pass

    async def get_bavg_score(
        self, likes: int, dislikes: int, prior_likes: int = 5, prior_dislikes: int = 5
    ) -> float:
        total_likes = likes + prior_likes
        total_votes = likes + dislikes + prior_likes + prior_dislikes

        if total_votes == 0:
            return 0.5

        return round(total_likes / total_votes, 3) * 10
    
    async def _get_channel_content(self, nickname: str):
        try:
            response = requests.get(f"https://t.me/s/{nickname}")
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, "html.parser")
                text = soup.get_text()
                cleaned_text = "\n".join(line.strip() for line in text.splitlines() if line.strip())
                return cleaned_text
            else:
                return None
        except Exception as e:
            log_manager.log_error(e, context={"_get_channel_content_func_error": str(e)})
            return {}


math_manager = MathManager()
