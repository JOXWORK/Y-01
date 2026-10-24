from __future__ import annotations

from typing import TYPE_CHECKING

import pytest_asyncio
from core.models.user import User
from fastapi_users.password import PasswordHelper

from tests.testing_core.test_depends import test_depends

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


@pytest_asyncio.fixture(scope="class", loop_scope="class")
async def class_create_db_user(class_session: AsyncSession):
    user_credentials = test_depends.user_credentials.register

    password = user_credentials.pop("password")
    user_credentials["hashed_password"] = PasswordHelper().hash(password)

    user = User(**user_credentials)

    class_session.add(user)
    await class_session.commit()

    yield

    await class_session.delete(user)
    await class_session.commit()
