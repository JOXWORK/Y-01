from sqlalchemy import select

from core.models.db_attach import db_attach
from core.models.moderation_rule import ModerationRule
from core.schemas.task_response import TaskResponseSchema
from core.taskiq.broker import broker
from core.taskiq.task_runtime_logger import task_runtime_logger


@broker.task
async def get_moderation_rules_micro_task(user_id: int) -> TaskResponseSchema:
    response = TaskResponseSchema(successful=False, content=None)

    try:
        async with db_attach.session_factory() as session:
            query = select(ModerationRule).where(ModerationRule.user_id == user_id)
            sqla_result = await session.execute(query)

            moderation_rule = sqla_result.scalar_one_or_none()

            if moderation_rule:
                response.content = {
                    "rules": moderation_rule.rules,
                    "rules_numbered": moderation_rule.rules_numbered,
                }
                response.successful = True
    except Exception:
        task_runtime_logger.logger.error("Get moderation rules micro task", exc_info=True)

    return response
