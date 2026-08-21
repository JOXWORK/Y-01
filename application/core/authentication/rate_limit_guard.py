from __future__ import annotations

import hashlib
import hmac
from functools import wraps
from typing import TYPE_CHECKING, Callable

from fastapi import HTTPException, status

from core.config import settings
from core.redis.rate_limit import r as ratelimit_redis

if TYPE_CHECKING:
    from redis.asyncio import Redis as AsyncRedis

    from core.models.user import User


class RateLimitGuard:
    def __init__(
        self,
        redis_client: AsyncRedis,
    ):
        self.redis_client = redis_client
        self.redis_formula = "rate_limit:%s:%s"  ## rate_limit:endpoint_name:user_identifier_digest

    def keep_rate_limit(self, kwarg_target: str = "user") -> Callable:
        def decorator(func: Callable) -> Callable:
            timeout = settings.rate_limit.rate_limit_test.timeout
            limit = settings.rate_limit.rate_limit_test.limit
            endpoint_name = settings.rate_limit.rate_limit_test.endpoint_name

            @wraps(func)
            async def wrapper(*args, **kwargs):
                idn_subject: User = kwargs[kwarg_target]
                user_id = idn_subject.id

                return await self._keep(
                    func,
                    args,
                    kwargs,
                    user_identifier=user_id,
                    endpoint_name=endpoint_name,
                    timeout=timeout,
                    limit=limit,
                )

            return wrapper

        return decorator

    async def _keep(
        self, func: Callable, args, kwargs, /, user_identifier: str | int, endpoint_name: str, timeout: int, limit: int
    ) -> any:
        query = await self._generate_redis_query(
            endpoint_name=endpoint_name,
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

    def _prototype_keep_user_identifier(
        self, user_identifier: str, endpoint_name: str, rate_limit: int, redis_ex: int
    ) -> Callable:
        def decorator(func: Callable) -> Callable:
            @wraps(func)
            async def wrapper(*args, **kwargs):
                if user_identifier_ := kwargs.get(user_identifier) is None:
                    raise Exception(f"User target identifier {user_identifier} not found in endpoint coroutine kwargs")

                user_idn = str(user_identifier_)

                query = await self._generate_redis_query(
                    endpoint_name=endpoint_name,
                    user_identifier=user_idn,
                )

                response = await self.redis_client.get(query)
                if response is not None:
                    count = int(response.encode())
                    if count >= rate_limit:
                        raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS)

                try:
                    result = await func(*args, **kwargs)
                except HTTPException as exc:
                    await self.redis_client.incr(query)
                    await self.redis_client.expire(name=query, time=redis_ex)

                    raise exc
                except Exception as exc:
                    raise exc

                await self.redis_client.incr(query)
                await self.redis_client.expire(name=query, time=redis_ex)

                return result

            return wrapper

        return decorator

    def endpoint_null_decorator(self, some_arg: str):
        def decorator(func):
            @wraps(func)
            async def wrapper(*args, **kwargs):
                print("Do before")
                result = await func(*args, **kwargs)
                print("Do after")

                return result

            return wrapper

        return decorator

    async def _generate_redis_query(
        self,
        endpoint_name: str,
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

        return self.redis_formula % (endpoint_name, user_identifier_digest.hexdigest())


rate_limit_guard = RateLimitGuard(redis_client=ratelimit_redis)
