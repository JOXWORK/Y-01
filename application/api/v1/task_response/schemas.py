from pydantic import BaseModel


class ResponseSchema(BaseModel):
    ready: bool
    content: dict


class UnsuccessfulResponseSchema(BaseModel):
    detail: str


class APITaskResponseSchema(BaseModel):
    ready: bool
    successful: bool | None
    content: dict | None
