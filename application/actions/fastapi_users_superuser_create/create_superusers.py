import asyncio
import contextlib

from api.dependencies.auth import get_user_db, get_user_manager
from core.authentication import UserManager
from core.models import db_attach
from core.models.user import User
from core.schemas.authentication import UserCreate
from fastapi_users.exceptions import UserAlreadyExists

from .superusers._superuser_Jingles import user as Jingles_user
from .superusers._superuser_JOXWORK import user as JOXWORK_user

get_context_user_db = contextlib.asynccontextmanager(get_user_db)
get_context_user_manager = contextlib.asynccontextmanager(get_user_manager)


async def create_user(
    user_create: UserCreate,
    user_manager: UserManager,
) -> User:
    return await user_manager.create(
        user_create=user_create,
        safe=False,
    )


async def create_operation(
    user_create: UserCreate,
    user_manager: UserManager,
) -> None:

    await create_user(
        user_create=user_create,
        user_manager=user_manager,
    )


async def main():
    users = [JOXWORK_user, Jingles_user]

    async with db_attach.session_factory() as session:
        async with get_context_user_db(session=session) as user_db:
            async with get_context_user_manager(user_db=user_db) as user_manager:
                for user_create in users:
                    try:
                        await create_operation(
                            user_create=user_create,
                            user_manager=user_manager,
                        )

                        print(f"User {user_create.email} successfully created")
                    except UserAlreadyExists:
                        print(f"User {user_create.email} already exists")
                    except Exception as exc:
                        print(exc)


if __name__ == "__main__":
    asyncio.run(main())
