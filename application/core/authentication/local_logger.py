import logging


class UserManagerLogger:
    def __init__(self):
        self.name = "user_manager"
        self.filename = f"{self.name}.log"
        self.log_level = logging.INFO

        logging.basicConfig(
            filename=self.filename,
            level=self.log_level,
        )

        self.logger = logging.getLogger(self.name)


user_manager_logger = UserManagerLogger()
