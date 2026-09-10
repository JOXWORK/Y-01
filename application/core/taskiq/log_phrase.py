from enum import Enum


class LogPhrase(str, Enum):
    UNEXPECTED_EXCEPTION = "Unexpected exception"
    SQLALCHEMY_EXCEPTION = "SQLAlchemy exception"
