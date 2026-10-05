import logging
from typing import Any

from core.config import settings
from core.taskiq.except_messages import TaskExceptionMessages


class TaskLogger(logging.Logger):
    def __init__(self, *args, **kwargs):
        name = settings.task_logger.name
        level = settings.task_logger.level

        super().__init__(name, level)

    def enum_error(self, msg: TaskExceptionMessages | Any, exc_info: bool = True, *args, **kwargs):
        message = msg
        if type(message) is TaskExceptionMessages:
            message = message.value

        self.error(msg=message, exc_info=exc_info, *args, **kwargs)


logging.setLoggerClass(TaskLogger)


def get_task_logger(name: str = settings.task_logger.name):
    return logging.getLogger(name)
