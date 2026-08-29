from pydantic import BaseModel


class ModerationRulesSchema(BaseModel):
    rules: dict[str, str]  # rule: action
