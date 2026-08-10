import redis.asyncio as redis

from core.config import settings

redis_cache = redis.from_url(
    settings.redis.cache.url,
)
