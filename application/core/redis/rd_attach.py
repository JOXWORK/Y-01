import redis.asyncio as redis

from core.config import settings


class RDAttach:
    def __init__(self, **kwargs):
        self.rd_names = []
        for rd_name, client in kwargs.items():
            setattr(self, rd_name, client)
            self.rd_names.append(rd_name)

    async def dispose(self) -> None:
        for rd_name in self.rd_names:
            client: redis.Redis = getattr(self, rd_name, None)

            if client is None:
                raise Exception(f'RDAttach dispose method got None on redis client name "{rd_name}"')

            await client.aclose()


rd_attach = RDAttach(
    rate_limit=redis.from_url(settings.redis.rate_limit.url),
)
