from __future__ import annotations

from typing import TYPE_CHECKING

from core.taskiq.result_backend import result_backend
from core.tasks.moderation_rules.schemas import TaskModerationRulesSchema
from core.tasks.moderation_rules.write_moderation_rules_db import write_moderation_rules_db_task

from .schemas import ModerationRulesSchema, TaskResult

if TYPE_CHECKING:
    from core.models.user import User


async def execute_write_moderation_rules_task(user_id: int, rules_schema: ModerationRulesSchema) -> str:
    task_rules_schema = TaskModerationRulesSchema(rules=rules_schema.rules)

    task = await write_moderation_rules_db_task.kiq(
        user_id=user_id,
        rules_schema=task_rules_schema,
    )

    return task.task_id


async def get_result_moderation_rules_task(task_id: str) -> TaskResult:
    task_is_ready = await result_backend.is_result_ready(task_id)

    successful = False
    if task_is_ready:
        task_result = await result_backend.get_result(task_id)
        if task_result.return_value:
            successful = True

    return {
        "is_ready": task_is_ready,
        "successful": successful,
    }
