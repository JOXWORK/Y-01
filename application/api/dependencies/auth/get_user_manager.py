from core.authentication import UserManager
from fastapi import Depends

from .get_user_db import get_user_db


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db=user_db)
