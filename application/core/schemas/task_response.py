from pydantic import BaseModel, ConfigDict


class TaskResponseSchema(BaseModel):
    model_config = ConfigDict(validate_assignment=True)

    successful: bool
    content: dict | None
