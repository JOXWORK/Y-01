from pydantic import BaseModel


class TaskIDSchema(BaseModel):
    task_id: str
