from core.models import db_attach
from core.models.moderation_rule import ModerationRule
from core.schemas.moderation_rules import ModerationRulesSchema
from core.taskiq.broker import broker
from sqlalchemy import select


@broker.task
async def write_moderation_rules_db_task(user_id: int, rules_schema: ModerationRulesSchema) -> bool:
    async with db_attach.session_factory() as session:
        query = select(ModerationRule).where(ModerationRule.user_id == user_id)
        sqla_result = await session.execute(query)
        moderation_rule = sqla_result.scalar_one_or_none()

        rules_dict = rules_schema.model_dump()

        if moderation_rule:
            moderation_rule.rules = rules_dict
        else:
            moderation_rule = ModerationRule(
                user_id=user_id,
                rules=rules_dict,
            )

            session.add(moderation_rule)

        await session.commit()

        return True
