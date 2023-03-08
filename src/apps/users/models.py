from sqlalchemy import (
    Column,
    String,
    Boolean,
)
from sqlalchemy.orm import relationship

from db.models import BaseModel


class User(BaseModel):
    """
    Модель пользователя
    """

    username = Column(String(15), nullable=False, unique=True, index=True)
    email = Column(String(30), nullable=False, unique=True, index=True)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean(), default=False)

    posts = relationship(
        "Post",
        back_populates="author",
        lazy="selectin",
        cascade="all, delete",
        passive_deletes=True,
    )
    posts_likes = relationship(
        "AssociationPostLikes",
        back_populates="user",
        lazy="selectin",
        cascade="all, delete",
        passive_deletes=True,
    )
