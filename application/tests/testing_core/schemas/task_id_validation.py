from pydantic import BaseModel


class TaskIDValidationSchema(BaseModel):
    task_id: str
