from fastapi_users import schemas

from core.types_own.user_id import UserIdType


class UserRead(schemas.BaseUser[UserIdType]):
    pass
