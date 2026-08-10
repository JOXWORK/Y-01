from pathlib import Path

from pydantic import BaseModel, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict

ROOT_DIR = Path(__file__).parent.parent


class HostSettings(BaseModel):
    host: str = "0.0.0.0"
    port: int = 8000

    uvc_reload: bool
    uvc_app_path: str = "main:app"
    uvc_workers: int


class ApiMainRouterSettings(BaseModel):
    prefix: str = "/api"


class ApiV1Prefix(BaseModel):
    router_v1: str = "/v1"
    hello_world: str = "/hello_world"
    auth: str = "/auth"

    @property
    def bearer_transport(self):
        # api/v1/auth/login

        return "".join(
            [
                ApiMainRouterSettings().prefix.replace("/", ""),
                self.router_v1,
                self.auth,
                "/login",
            ]
        )


class ApiV1Tags(BaseModel):
    hello_world: list[str] = ["Test routes"]
    auth: list[str] = ["Auth"]


class ApiV1Summary(BaseModel):
    hello_world: str = "This is a test router, take an order"


class ApiV1Subs(BaseModel):
    prefix: ApiV1Prefix = ApiV1Prefix()
    tags: ApiV1Tags = ApiV1Tags()
    summary: ApiV1Summary = ApiV1Summary()


class ApiCustoms(BaseModel):
    v1: ApiV1Subs = ApiV1Subs()
    main_router: ApiMainRouterSettings = ApiMainRouterSettings()


class DBSettings(BaseModel):
    url: PostgresDsn
    echo: bool
    echo_pool: bool = False
    pool_size: int = 50
    max_overflow: int = 20
    naming_convention: dict[str, str] = {
        "ix": "ix_%(table_name)s__%(column_0_N_name)s",
        "uq": "uq_%(table_name)s__%(column_0_N_name)s",
        "ck": "ck_%(table_name)s__%(constraint_name)s",
        "fk": "fk_%(table_name)s__%(column_0_N_name)s__%(referred_table_name)s__%(referred_column_0_N_name)s",
        "pk": "pk_%(table_name)s__%(column_0_N_name)s",
    }


class RedisConfig(BaseModel):
    url: str
    ttl: int


class RedisDB(BaseModel):
    cache: RedisConfig
    taskiq: RedisConfig


class TaskiqBroker(BaseModel):
    maxlen: int = 10_000
    approximate: bool = True


class TaskiqResultBackend(BaseModel):
    result_ex_time: int = 3600  # sec


class TaskiqConfig(BaseModel):
    broker: TaskiqBroker = TaskiqBroker()
    result_backend: TaskiqResultBackend = TaskiqResultBackend()


class AccessToken(BaseModel):
    lifetime_seconds: int = 3600

    reset_password_token_secret: str
    verification_token_secret: str


class UserSession(BaseModel):
    lifetime_minutes: float = 0
    lifetime_hours: float = 0
    lifetime_days: float = 7
    reissue_max_amount: int = 51  # strict: x == reissue_max_amount -> error


class RefreshToken(BaseModel):
    hmac_secret: str


class AuthSettings(BaseModel):
    access_token: AccessToken
    refresh_token: RefreshToken
    user_session: UserSession = UserSession()


class OAuth2PasswordBearerSchemeSettings(BaseModel):
    auto_error: bool = False


class HTTPBearerSchemeSettings(BaseModel):
    auto_error: bool = False


class Settings(BaseSettings):
    ROOT_DIR: Path = ROOT_DIR

    model_config = SettingsConfigDict(
        env_file=(
            ".env.template",
            ".env",
        ),
        env_file_encoding="UTF-8",
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="APPLICATION__",
    )

    api: ApiCustoms = ApiCustoms()

    host: HostSettings

    db: DBSettings

    redis: RedisDB

    taskiq: TaskiqConfig = TaskiqConfig()

    auth: AuthSettings


## Допустимо передовать в env_file кортеж из нескольких .env файлов, перегружающих друг друга и значения конфига.
## Например, env_file=(".env", ".env.template"). В .env указывается secrets информация, перегружая информацию из .env.template.
## Такой подход удобен для загрузки файлов конфига в репозиторий, не раскрывая secrets информацию.

settings = Settings()
