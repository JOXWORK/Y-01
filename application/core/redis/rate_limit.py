import redis.asyncio as redis

from core.config import settings

r = redis.from_url(
    settings.redis.rate_limit.url,
)
