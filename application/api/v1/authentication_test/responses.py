from pydantic import BaseModel


class SuccessfulResponse(BaseModel):
    successful: bool


class IsUserValidResponse(BaseModel):
    is_valid: bool
