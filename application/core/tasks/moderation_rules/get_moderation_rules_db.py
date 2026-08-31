from core.models import db_attach
from core.models.moderation_rule import ModerationRule
from core.taskiq.broker import broker
from sqlalchemy import select


@broker.task
async def get_moderation_rules_db_task(user_id: int) -> dict[str, str]:
    async with db_attach.session_factory() as session:
        query = select(ModerationRule).where(ModerationRule.user_id == user_id)
        sqla_result = await session.execute(query)

        moderation_rule = sqla_result.scalar_one_or_none()

        if moderation_rule is None:
            return None

        return moderation_rule.rules
