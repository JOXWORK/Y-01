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


class URLS(ApiV1Prefix):
    root: str = "http://app:8000/api/v1"

    def model_post_init(self, __context):
        super().model_post_init(__context)

        for name, body in ApiV1Prefix().model_dump().items():
            setattr(self, name, lambda endpoint_name, body=body: self.root + body + endpoint_name)

    def endpoint(self, endpoint_name: str) -> str:
        return self.root + endpoint_name


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
