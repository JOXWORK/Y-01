from pydantic import BaseModel, ConfigDict


class SetResponseSchema(BaseModel):
    is_ready: bool
    successful: bool


class TaskIDSchema(BaseModel):
    task_id: str


class GetResponseSchema(BaseModel):
    model_config = ConfigDict(validate_assignment=True)

    is_ready: bool
    rules: dict[str, str] | None
