from core.config import settings
from core.schemas.task_response import TaskResponseSchema
from core.taskiq.broker import broker
from core.taskiq.log_phrase import LogPhrase
from core.taskiq.task_runtime_logger import task_runtime_logger
from taskiq.exceptions import TaskiqError

from .get_moderation_rules_db import get_moderation_rules_db_task


@broker.task
async def get_human_readable_moderation_rules_db_task(user_id: int) -> TaskResponseSchema:
    response = TaskResponseSchema(successful=False, content=None)
    try:
        task = await get_moderation_rules_db_task.kiq(user_id)

        task_result = await task.wait_result(timeout=settings.taskiq.result_timeout)
        return_value = task_result.return_value

        if return_value.successful:
            rules_dict = return_value.content
            human_reabale_rules_dict = {}

            for index, rule_acion_dict in rules_dict["rules"].items():
                human_reabale_rules_dict.update(rule_acion_dict)

            response.content = {"rules": human_reabale_rules_dict}
            response.successful = True

    except TaskiqError:
        task_runtime_logger.logger.error("Taskiq runtime task error", exc_info=True)
    except Exception:
        task_runtime_logger.logger.error(LogPhrase.UNEXPECTED_EXCEPTION.value, exc_info=True)

    return response
