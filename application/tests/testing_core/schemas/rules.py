from pydantic import BaseModel


class RulesSchema(BaseModel):
    rules: dict[str, str]
    rules_numbered: dict[str, dict[str, str]]
