from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    TIMESTAMP,
)
from sqlalchemy.orm import (
    declarative_base,
    declared_attr,
)

Model = declarative_base()


class BaseModel(Model):
    """
    Класс базовой модели
    """

    __abstract__ = True
    id = Column(
        Integer,
        nullable=False,
        unique=True,
        primary_key=True,
        autoincrement=True,
        index=True,
    )
    created_at = Column(
        TIMESTAMP,
        nullable=False,
        default=datetime.now,
    )
    updated_at = Column(
        TIMESTAMP,
        nullable=False,
        default=datetime.now,
        onupdate=datetime.now,
    )

    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()
