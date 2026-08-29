from pydantic import BaseModel


class ReadySuccessResponseSchema(BaseModel):
    is_ready: bool
    successful: bool
