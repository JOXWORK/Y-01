from api.service.rules.numerate_dict import numerate_dict
from pydantic import BaseModel


class RulesSchema(BaseModel):
    rules: dict[str, str] = {
        "запрещена реклама": "ban",
        "запрещен спам": "mute",
        "запрещены оскорбления": "жick",
        "запрещена скрытая реклама": "ban",
        "запрещена реклама профиля": "ban",
        "запрещена реклама 18+ и не легальных ресурсов": "ban",
        "запрещена реклама игорных сервисов": "ban",
    }

    rules_numbered: dict[str, dict[str, str]] = numerate_dict({"rules": rules}).pop("rules_numbered")
