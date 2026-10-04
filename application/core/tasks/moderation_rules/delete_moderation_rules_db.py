from core.models.db_attach import db_attach
from core.models.moderation_rule import ModerationRule
from core.schemas.task_response import TaskResponseSchema
from core.taskiq.broker import broker
from core.taskiq.except_messages import TaskExceptionMessages
from core.taskiq.task_messages import TaskResponseMessages, create_message
from core.taskiq.task_runtime_logger import task_runtime_logger
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError


@broker.task
async def delete_moderation_rules_db_task(user_id: int) -> TaskResponseSchema:
    response = TaskResponseSchema(successful=False, content=None)

    try:
        async with db_attach.session_factory() as session:
            query = select(ModerationRule).where(ModerationRule.user_id == user_id)
            sqla_result = await session.execute(query)
            moderation_rule = sqla_result.scalar_one_or_none()

            if moderation_rule:
                await session.delete(moderation_rule)
                await session.commit()

                response.successful = True
            else:
                response.content = create_message(message=TaskResponseMessages.RULES_NOT_FOUND)

    except SQLAlchemyError:
        task_runtime_logger.logger.error(
            TaskExceptionMessages.SQLALCHEMY_EXCEPTION.value,
            exc_info=True,
        )

    except Exception:
        task_runtime_logger.logger.error(
            TaskExceptionMessages.UNEXPECTED_EXCEPTION.value,
            exc_info=True,
        )

    return response
