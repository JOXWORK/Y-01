from core.models import db_attach
from core.models.moderation_rule import ModerationRule
from core.schemas.task_response import TaskResponseSchema
from core.taskiq.broker import broker
from core.taskiq.except_messages import TaskExceptionMessages
from core.taskiq.task_logger import get_task_logger
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

logger = get_task_logger()


@broker.task
async def set_moderation_rules_db_task(user_id: int, rules: dict, rules_numbered: dict) -> TaskResponseSchema:
    response = TaskResponseSchema(successful=False, content=None)

    try:
        async with db_attach.session_factory() as session:
            query = select(ModerationRule).where(ModerationRule.user_id == user_id)
            sqla_result = await session.execute(query)
            moderation_rule = sqla_result.scalar_one_or_none()

            if moderation_rule:
                moderation_rule.rules = rules
                moderation_rule.rules_numbered = rules_numbered
            else:
                moderation_rule = ModerationRule(
                    user_id=user_id,
                    rules=rules,
                    rules_numbered=rules_numbered,
                )

                session.add(moderation_rule)

            await session.commit()

        response.successful = True
    except SQLAlchemyError:
        logger.enum_error(TaskExceptionMessages.SQLALCHEMY_EXCEPTION)
    except Exception:
        logger.enum_error(TaskExceptionMessages.UNEXPECTED_EXCEPTION)

    return response
