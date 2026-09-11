from enum import Enum, EnumType


class TaskResponseMessages(str, Enum):
    RULES_NOT_FOUND = "Rules not found"


def create_message(message: EnumType) -> dict[str, EnumType]:
    return {"message": message}
