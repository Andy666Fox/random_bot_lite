import os

import requests
from bs4 import BeautifulSoup
from groq import Groq
from utils.globals import LLM_ROLE_DESCRIPTION
from utils.log_manager import log_manager


async def _get_channel_content(nickname: str):
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


async def _get_llm_answer(content: str):
    try:
        client = Groq(api_key=os.getenv("GROQ_API_KEY"))

        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": LLM_ROLE_DESCRIPTION},
                {
                    "role": "user",
                    "content": content,
                },
            ],
            model="llama-3.3-70b-versatile",
        )
        answer = chat_completion.choices[0].message.content
        return answer
    except Exception as e:
        log_manager.log_error(e, context={"_get_llm_answer_func_error": str(e)})
        return {}


async def get_summary(nickname: str):
    try:
        content = await _get_channel_content(nickname)
        if content:
            summary = await _get_llm_answer(content)
            return summary
        else:
            return None
    except Exception as e:
        log_manager.log_error(e, context={"get_summary_func_error": str(e)})
        return {}
