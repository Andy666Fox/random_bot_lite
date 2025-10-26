from groq import Groq
from bs4 import BeautifulSoup
import requests
import os
from service.default_answers import LLM_ROLE_DESCRIPTION
from service.log_manager import bot_logger

async def _get_channel_content(nickname: str):
    try:
        response = requests.get(f'https://t.me/s/{nickname}')
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            text = soup.get_text()
            cleaned_text = '\n'.join(line.strip() for line in text.splitlines() if line.strip())
            return cleaned_text
        else:
            print(f"Error: {response.status_code}")
            return None
    except Exception as e:
        bot_logger.log_error(e, context={"_get_channel_content_func_error": str(e)})
        return {}

async def _get_llm_answer(content: str):
    try:
        client = Groq(api_key=os.getenv('GROQ_API_KEY'))

        chat_completion = client.chat.completions.create(
        messages=[
            # Set an optional system message. This sets the behavior of the
            # assistant and can be used to provide specific instructions for
            # how it should behave throughout the conversation.
            {
                "role": "system",
                "content": LLM_ROLE_DESCRIPTION
            },
            # Set a user message for the assistant to respond to.
            {
                "role": "user",
                "content": content,
            }
        ],

        # The language model which will generate the completion.
        model="llama-3.3-70b-versatile"
        )
        answer = chat_completion.choices[0].message.content
        return answer
    except Exception as e:
        bot_logger.log_error(e, context={"_get_llm_answer_func_error": str(e)})
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
        bot_logger.log_error(e, context={"get_summary_func_error": str(e)})
        return {}