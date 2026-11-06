from pydantic import BaseModel


class TaskMessageValidationSchema(BaseModel):
    message: str
