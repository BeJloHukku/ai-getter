from google import genai
from google.genai.types import GenerateContentConfig, HttpOptions
import asyncio

from config import config_obj

client = genai.Client(http_options=HttpOptions(api_version="v1"), api_key=config_obj.gemini_api_key)
model_id = "gemini-2.5-flash"


async def generate_text():
    response = await client.aio.models.generate_content(
            model=model_id,
            contents="Привет, напиши, какой сегодня день",
        )

    return response.text if response else None

print(asyncio.run(generate_text()))
