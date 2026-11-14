from pydantic import BaseModel


class TaskMessageSchema(BaseModel):
    message: str
