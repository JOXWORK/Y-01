import logging


class TaskRuntimeLogger:
    def __init__(self):
        self.name = "task_runtime_logger"
        self.log_level = logging.INFO

        logging.basicConfig(level=self.log_level)

        self.logger = logging.getLogger(self.name)


task_runtime_logger = TaskRuntimeLogger()
