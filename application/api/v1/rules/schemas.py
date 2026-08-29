from pydantic import BaseModel


class ModerationRulesSchema(BaseModel):
    rules: dict[str, str]  # rule: action


class TaskIDSchema(BaseModel):
    task_id: str


class TaskResult(BaseModel):
    is_ready: bool
    successful: bool
