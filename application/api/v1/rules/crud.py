from core.schemas.moderation_rules import ModerationRulesSchema
from core.tasks.moderation_rules.get_moderation_rules_db import get_moderation_rules_db_task
from core.tasks.moderation_rules.set_moderation_rules_db import set_moderation_rules_db_task

from api.schemas.v1.task_id import TaskIDSchema


async def set_request(user_id: int, rules_schema: ModerationRulesSchema) -> TaskIDSchema:
    task = await set_moderation_rules_db_task.kiq(
        user_id=user_id,
        rules_schema=rules_schema,
    )

    return TaskIDSchema(task_id=task.task_id)


async def get_request(user_id: int) -> TaskIDSchema:
    task = await get_moderation_rules_db_task.kiq(user_id)

    return TaskIDSchema(task_id=task.task_id)
