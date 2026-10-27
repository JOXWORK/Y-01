from secrets import token_hex

from core.config import ApiV1Prefix
from pydantic import BaseModel


def generate_username() -> str:
    return f"test_user_{token_hex(8)}@e.com"


class UserCredentials(BaseModel):
    username: str
    password: str
    is_superuser: bool

    @property
    def register(self) -> dict:
        return {
            "email": self.username,
            "password": self.password,
            "is_active": True,
            "is_superuser": self.is_superuser,
            "is_verified": True,
        }

    @property
    def login(self) -> dict:
        return {
            "username": self.username,
            "password": self.password,
        }


class URLS(BaseModel):
    root: str = "http://app:8000/api/v1"

    prefix: ApiV1Prefix = ApiV1Prefix()

    def model_post_init(self, __context):
        super().model_post_init(__context)

        prefix = ApiV1Prefix()

        for name, body in prefix.model_dump().items():
            setattr(prefix, name, lambda endpoint_name, root=self.root, body=body: root + body + endpoint_name)

        self.prefix = prefix


class TestDepends(BaseModel):
    __test__ = False

    user_credentials: UserCredentials = UserCredentials(
        username=generate_username(),
        password=token_hex(),
        is_superuser=False,
    )

    superuser_credentials: UserCredentials = UserCredentials(
        username=generate_username(),
        password=token_hex(),
        is_superuser=True,
    )

    urls: URLS = URLS()


test_depends = TestDepends()
