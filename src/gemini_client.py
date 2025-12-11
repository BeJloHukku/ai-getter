from google import genai
from google.genai.types import GenerateContentConfig, HttpOptions
import asyncio

from config import config_obj
from src.exeptions import AiGeminiError, NoResponseWasGivenFromGeminiError

client = genai.Client(http_options=HttpOptions(api_version="v1"), api_key=config_obj.gemini_api_key)
model_id = "gemini-2.5-flash"


async def get_answer_from_gemini(prompt: str):
    try:
        response = await client.aio.models.generate_content(
                model=model_id,
                contents=prompt,
            )
    except Exception:
        raise AiGeminiError

    if not response:
        raise NoResponseWasGivenFromGeminiError
    
    return response.text


