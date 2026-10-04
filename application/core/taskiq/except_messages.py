from enum import Enum


class TaskExceptionMessages(str, Enum):
    UNEXPECTED_EXCEPTION = "Unexpected exception"
    SQLALCHEMY_EXCEPTION = "SQLAlchemy exception"
