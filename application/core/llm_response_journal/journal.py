from datetime import timedelta

from redis.asyncio import Redis
from redis.exceptions import RedisError

from core.config import settings
from core.redis.rd_attach import rd_attach


class LLMResponseJournalWriteError(Exception):
    pass


class LLMResponseJournal:
    def __init__(
        self,
        lifetime_days: int,
        lifetime_hours: int,
    ):
        self.lifetime_days = lifetime_days
        self.lifetime_hours = lifetime_hours

        self.expire_timedelta = timedelta(
            days=self.lifetime_days,
            hours=self.lifetime_hours,
        )

        self.redis_client: Redis = rd_attach.llm_response_journal

    async def write(self, key_name: str, content: str) -> None:
        try:
            await self.redis_client.set(name=key_name, value=content)
            await self.redis_client.expire(
                name=key_name,
                time=int(self.expire_timedelta.total_seconds()),
            )
        except RedisError as exc:
            raise LLMResponseJournalWriteError(str(exc))


llm_response_journal = LLMResponseJournal(
    lifetime_days=settings.llm_response_journal.lifetime_days,
    lifetime_hours=settings.llm_response_journal.lifetime_hours,
)
