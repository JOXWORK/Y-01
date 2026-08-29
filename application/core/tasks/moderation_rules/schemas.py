from pydantic import BaseModel


class TaskModerationRulesSchema(BaseModel):
    rules: dict[str, str]
