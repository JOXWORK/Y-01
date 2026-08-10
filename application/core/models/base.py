from sqlalchemy import MetaData
from sqlalchemy.orm import (
    DeclarativeBase,
    declared_attr,
)
from utils.case_transform import transform

from core.config import settings


class Base(DeclarativeBase):
    __abstract__ = True

    metadata = MetaData(naming_convention=settings.db.naming_convention)

    @declared_attr.directive
    def __tablename__(cls):
        snake_case_name = transform(line=cls.__name__)
        return f"{snake_case_name}s"
