from pydantic import BaseModel


class TokenRefreshSchema(BaseModel):
    refresh_token: str
