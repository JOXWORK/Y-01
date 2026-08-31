from pydantic import BaseModel


class ModerationResponseNotReadySchema(BaseModel):
    not_ready: bool = True
