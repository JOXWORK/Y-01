from pydantic import BaseModel


class RulesValidationSchema(BaseModel):
    rules: dict[str, str]
    rules_numbered: dict[str, dict[str, str]]
