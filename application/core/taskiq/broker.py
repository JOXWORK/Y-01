from taskiq_redis import RedisStreamBroker

from core.config import settings

from .result_backend import result_backend

broker = RedisStreamBroker(
    url=settings.redis.taskiq.url,
    maxlen=settings.taskiq.broker.maxlen,
    approximate=settings.taskiq.broker.approximate,
).with_result_backend(result_backend)
