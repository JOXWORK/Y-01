from pydantic import BaseModel


class TaskModerationRulesSchema(BaseModel):
    rules: dict[str, str]


class TaskModerationRulesReturnSchema(BaseModel):
    successful: bool
