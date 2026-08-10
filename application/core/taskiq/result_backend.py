from taskiq_redis import RedisAsyncResultBackend

from core.config import settings

result_backend = RedisAsyncResultBackend(
    redis_url=settings.redis.taskiq.url,
    result_ex_time=settings.taskiq.result_backend.result_ex_time,
)
