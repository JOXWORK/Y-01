from openai import AsyncOpenAI

from core.config import settings

openai_client = AsyncOpenAI(
    base_url=settings.cloud_ru_api.url,
    api_key=settings.cloud_ru_api.key.get_secret_value(),
)
