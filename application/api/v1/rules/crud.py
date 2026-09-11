from core.tasks.moderation_rules.get_moderation_rules_db import get_moderation_rules_db_task
from core.tasks.moderation_rules.set_moderation_rules_db import set_moderation_rules_db_task

from api.schemas.v1.task_id import TaskIDSchema

from .service.numerate_dict import numerate_dict


async def create_request(user_id: int, rules: dict) -> TaskIDSchema:
    rules_numbered = numerate_dict(rules)

    task = await set_moderation_rules_db_task.kiq(
        user_id=user_id,
        rules=rules,
        rules_numbered=rules_numbered,
    )

    return TaskIDSchema(task_id=task.task_id)


async def get_request(user_id: int) -> TaskIDSchema:
    task = await get_moderation_rules_db_task.kiq(user_id)

    return TaskIDSchema(task_id=task.task_id)
