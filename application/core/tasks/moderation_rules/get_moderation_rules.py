from core.schemas.task_response import TaskResponseSchema
from core.task_depends.get_moderation_rules import getModerationRules
from core.taskiq.broker import broker
from core.taskiq.except_messages import TaskExceptionMessages
from core.taskiq.task_logger import get_task_logger
from core.taskiq.task_messages import TaskResponseMessages, create_message
from sqlalchemy.exc import SQLAlchemyError

logger = get_task_logger()


@broker.task
async def GetModerationRules(user_id: int) -> TaskResponseSchema:
    response = TaskResponseSchema(successful=False, content=None)
    try:
        moderation_rules = await getModerationRules(user_id)

        if moderation_rules:
            content = {}
            content.update(moderation_rules)

            response.content = content
            response.successful = True
        else:
            response.content = create_message(TaskResponseMessages.RULES_NOT_FOUND)
    except SQLAlchemyError:
        logger.enum_error(TaskExceptionMessages.SQLALCHEMY_EXCEPTION)
    except Exception:
        logger.enum_error(TaskExceptionMessages.UNEXPECTED_EXCEPTION)

    return response
