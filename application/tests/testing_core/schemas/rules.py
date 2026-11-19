from enum import Enum

from api.service.rules.numerate_dict import numerate_dict
from pydantic import BaseModel, ConfigDict, model_validator


class RULES_ENUM(Enum):
    RULES = {
        "запрещена реклама": "ban",
        "запрещен спам": "mute",
        "запрещены оскорбления": "жick",
        "запрещена скрытая реклама": "ban",
        "запрещена реклама профиля": "ban",
        "запрещена реклама 18+ и не легальных ресурсов": "ban",
        "запрещена реклама игорных сервисов": "ban",
    }

    RULES_NUMBERED = numerate_dict(RULES)


class RulesModel(BaseModel):
    rules: dict[str, str] = RULES_ENUM.RULES.value
    rules_numbered: dict[str, dict[str, str]] = RULES_ENUM.RULES_NUMBERED.value


class RulesValidationSchema(BaseModel):
    model_config = ConfigDict(extra="forbid")

    rules: dict[str, str] = RULES_ENUM.RULES.value
    rules_numbered: dict[str, dict[str, str]] = RULES_ENUM.RULES_NUMBERED.value

    @model_validator(mode="before")
    @classmethod
    def validate_dicts(cls, data):
        if isinstance(data, dict):
            data: dict
            rules = data.get("rules")
            rules_numbered = data.get("rules_numbered")

            if rules != RULES_ENUM.RULES.value:
                raise ValueError(f"Input rules is not compare installed rules [input={rules}]")
            if rules_numbered != RULES_ENUM.RULES_NUMBERED.value:
                raise ValueError(f"Input numbered rules is not compare installed numbered rules [input={rules_numbered}]")

            return data

        raise ValueError("Input data should be a dicatonary type")
