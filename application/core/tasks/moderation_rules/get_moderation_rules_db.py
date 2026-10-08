from core.schemas.task_response import TaskResponseSchema
from core.taskiq.broker import broker
from core.taskiq.except_messages import TaskExceptionMessages
from core.taskiq.task_logger import get_task_logger
from core.taskiq.task_messages import TaskResponseMessages, create_message
from core.tasks.micro_tasks.micro_get_moderation_rules import get_moderation_rules_micro_task

logger = get_task_logger()


@broker.task
async def get_moderation_rules_db_task(user_id: int) -> TaskResponseSchema:
    response = TaskResponseSchema(successful=False, content=None)
    try:
        rules_micro_task = await get_moderation_rules_micro_task.kiq(user_id)
        rules_micro_task_result = await rules_micro_task.wait_result()
        rules_micro_task_response = rules_micro_task_result.return_value

        if rules_micro_task_response.successful:
            response_content = rules_micro_task_response.content
            content = {}

            content.update(response_content["rules"])
            content.update(response_content["rules_numbered"])

            response.content = content
            response.successful = True
        else:
            response.content = create_message(TaskResponseMessages.RULES_NOT_FOUND)
    except Exception:
        logger.enum_error(TaskExceptionMessages.UNEXPECTED_EXCEPTION)

    return response
