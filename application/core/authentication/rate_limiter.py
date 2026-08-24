from __future__ import annotations

import hashlib
import hmac
from functools import wraps
from typing import TYPE_CHECKING

from fastapi import HTTPException, status

from core.config import settings
from core.redis.rate_limit import r as ratelimit_redis

if TYPE_CHECKING:
    from typing import Callable

    from redis.asyncio import Redis as AsyncRedis

    from core.config import RateLimitEndpoint, RateLimitSettings


class RateLimiter:
    def __init__(
        self,
        redis_client: AsyncRedis,
        config: RateLimitSettings,
    ):
        self.redis_client = redis_client
        self.redis_formula = "rate_limit:%s:%s"  ## rate_limit:operation_name:user_identifier_digest
        self.config = config

    def restrain(self, kwarg_schema: str, endpoint_cfg: RateLimitEndpoint):
        def decorator(func: Callable) -> Callable:
            @wraps(func)
            async def wrapper(*args, **kwargs):
                auth_sub = await self._get_auth_sub(
                    kwargs=kwargs,
                    kwarg_schema=kwarg_schema,
                )

                return await self._restrain(
                    func,
                    args,
                    kwargs,
                    user_identifier=auth_sub,
                    operation_name=func.__name__,
                    timeout=endpoint_cfg.timeout,
                    limit=endpoint_cfg.limit,
                )

            return wrapper

        return decorator

    async def _restrain(
        self, func: Callable, args, kwargs, /, user_identifier: str | int, operation_name: str, timeout: int, limit: int
    ) -> any:
        query = await self._generate_redis_query(
            operation_name=operation_name,
            user_identifier=user_identifier,
        )

        response = await self.redis_client.get(query)
        if response:
            count = int(response.decode())
            if count >= limit:
                raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS)

        try:
            result = await func(*args, **kwargs)
        finally:
            await self.redis_client.incr(query)
            await self.redis_client.expire(name=query, time=timeout)

        return result

    async def _generate_redis_query(
        self,
        operation_name: str,
        user_identifier: str | int,
        *,
        key: str = settings.rate_limit.hmac_secret,
        digestmod=hashlib.sha256,
    ) -> str:
        user_identifier_ = str(user_identifier)

        user_identifier_digest = hmac.new(
            key=key.encode(),
            msg=user_identifier_.encode(),
            digestmod=digestmod,
        )

        return self.redis_formula % (operation_name, user_identifier_digest.hexdigest())

    async def _get_auth_sub(self, kwargs: dict, kwarg_schema: str) -> any:
        kwarg_way = kwarg_schema.split(".")
        auth_sub = kwargs[kwarg_way[0]]

        if len(kwarg_way) == 1:
            return auth_sub

        for layer in kwarg_way[1:]:
            auth_sub = getattr(auth_sub, layer, None)

        if auth_sub is None:
            raise Exception(f"Got None auth_sub for {kwarg_schema}")

        return auth_sub


rate_limiter = RateLimiter(
    redis_client=ratelimit_redis,
    config=settings.rate_limit,
)
