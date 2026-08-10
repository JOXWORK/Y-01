from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy.ext.asyncio import (
    async_sessionmaker,
    create_async_engine,
)

from core.config import settings

if TYPE_CHECKING:
    from typing import AsyncGenerator

    from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession

## Database tools


class DBAttach:
    def __init__(
        self,
        url: str,
        echo: bool = False,
        echo_pool: bool = False,
        pool_size: int = 5,
        max_overflow: int = 10,
    ) -> None:
        self.engine: AsyncEngine = create_async_engine(
            url=url,
            echo=echo,
            echo_pool=echo_pool,
            pool_size=pool_size,
            max_overflow=max_overflow,
        )

        self.session_factory: async_sessionmaker[AsyncSession] = async_sessionmaker(
            bind=self.engine,
            expire_on_commit=False,
            autoflush=False,
            autocommit=False,
        )

    async def dispose(self) -> None:
        await self.engine.dispose()

    async def new_session(self) -> AsyncGenerator[AsyncSession, None]:
        async with self.session_factory() as session_obj:
            yield session_obj


db_attach = DBAttach(
    url=str(settings.db.url),
    echo=settings.db.echo,
    echo_pool=settings.db.echo_pool,
    pool_size=settings.db.pool_size,
    max_overflow=settings.db.max_overflow,
)
