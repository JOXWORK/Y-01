from pydantic import BaseModel


class ModerationLLMResponseSchema(BaseModel):
    rule: str | None
