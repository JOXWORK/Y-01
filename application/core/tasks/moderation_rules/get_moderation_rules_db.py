from core.schemas.task_response import TaskResponseSchema
from core.taskiq.broker import broker
from core.taskiq.task_messages import TaskResponseMessages, create_message
from core.taskiq.task_runtime_logger import task_runtime_logger
from core.tasks.micro_tasks.micro_get_moderation_rules import get_moderation_rules_micro_task


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
        task_runtime_logger.logger.error("Unexpected exception", exc_info=True)

    return response
