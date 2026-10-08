from sqlalchemy import select

from core.models.db_attach import db_attach
from core.models.moderation_rule import ModerationRule
from core.taskiq.task_logger import get_task_logger

logger = get_task_logger()


async def getModerationRules(user_id: int) -> dict | None:
    async with db_attach.session_factory() as session:
        query = select(ModerationRule).where(ModerationRule.user_id == user_id)
        sqla_result = await session.execute(query)

        moderation_rule = sqla_result.scalar_one_or_none()

        if not moderation_rule:
            return None

        return {
            "rules": moderation_rule.rules,
            "rules_numbered": moderation_rule.rules_numbered,
        }
