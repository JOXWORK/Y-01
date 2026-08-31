from pydantic import BaseModel


class ModerationResponseSchema(BaseModel):
    rule: str
