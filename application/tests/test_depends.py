from secrets import token_hex

from pydantic import BaseModel


class UserCredentials(BaseModel):
    username: str
    password: str

    @property
    def register(self) -> dict:
        return {
            "email": self.username,
            "password": self.password,
            "is_active": True,
            "is_superuser": True,
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

    def endpoint(self, endpoint_name: str) -> str:
        return self.root + endpoint_name


class TestDepends(BaseModel):
    __test__ = False

    mixin: str = token_hex(8)

    username: str = f"test_{mixin}@e.com"
    password: str = "qwerty"

    user_credentials: UserCredentials = UserCredentials(
        username=username,
        password=password,
    )

    urls: URLS = URLS()


test_depends = TestDepends()
