from core.models import db_attach
from core.models.moderation_rule import ModerationRule
from core.schemas.task_response import TaskResponseSchema
from core.taskiq.broker import broker
from core.taskiq.task_runtime_logger import task_runtime_logger
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError


@broker.task
async def get_moderation_rules_db_task(user_id: int) -> TaskResponseSchema:
    response = TaskResponseSchema(successful=False, content=None)
    try:
        async with db_attach.session_factory() as session:
            query = select(ModerationRule).where(ModerationRule.user_id == user_id)
            sqla_result = await session.execute(query)

            moderation_rule = sqla_result.scalar_one_or_none()

            content = {"message": "Rules not found"}
            if moderation_rule:
                content.clear()

                content.update(moderation_rule.rules)
                content.update(moderation_rule.rules_numbered)

            response.content = content
            response.successful = True
    except SQLAlchemyError:
        task_runtime_logger.logger.error("SQLAlchemy exception", exc_info=True)
    except Exception:
        task_runtime_logger.logger.error("Unexpected exception", exc_info=True)

    return response
