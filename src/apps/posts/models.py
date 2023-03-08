import uuid

from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from db.models import BaseModel


class AssociationPostLikes(BaseModel):
    user_id = Column(ForeignKey("user.id", ondelete="CASCADE"), primary_key=True)
    post_id = Column(ForeignKey("post.id", ondelete="CASCADE"), primary_key=True)

    user = relationship("User", back_populates="posts_likes")
    post = relationship("Post", back_populates="users_likes")


class Post(BaseModel):
    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(20), nullable=False, unique=True)
    description = Column(String(50), nullable=False)
    author_id = Column(
        Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False
    )
    like_count = Column(Integer, default=0)

    author = relationship("User", back_populates="posts", lazy="selectin")
    users_likes = relationship(
        "AssociationPostLikes",
        back_populates="post",
        lazy="selectin",
        cascade="all, delete",
        passive_deletes=True,
    )
