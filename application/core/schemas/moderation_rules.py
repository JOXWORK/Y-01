from pydantic import BaseModel


class ModerationRulesSchema(BaseModel):
    rules: dict[str, str]  # rule: action


class RulesSchema(ModerationRulesSchema):
    rules_numbered: dict[str, dict[str, str]]
