from pydantic import BaseModel


class ModerationRulesSchema(BaseModel):
    rules: dict[str, str]  # rule: action


class TaskIDSchema(BaseModel):
    task_id: str


class TaskReadySuccessResult(BaseModel):
    is_ready: bool
    successful: bool
