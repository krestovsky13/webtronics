from typing import (
    Optional,
    Any,
)

from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.exceptions import (
    AlreadyExistException,
    DoesNotExistException,
)
from db.repository import BaseRepository
from apps.posts.models import (
    Post,
    AssociationPostLikes,
)
from apps.posts.schemas import (
    PostCreate,
    PostBase,
)
from apps.users.models import User


class PostServices(BaseRepository[Post, PostCreate, PostBase]):
    """
    Класс операций с постами
    """

    def __init__(self):
        super().__init__(Post)

    async def create(self, obj: PostCreate, db: AsyncSession) -> Optional[Post]:
        """
        Создание поста
        """
        # Проверяем уникальность заголовка
        if await db.scalar(select(Post).filter(Post.title == obj.title)):
            raise AlreadyExistException(Post)

        return await super().create(obj, db)

    async def create_with_author(
        self, post: PostBase, user: User, db: AsyncSession
    ) -> Post:
        post = PostCreate(**post.dict(), author_id=user.id)

        return await self.create(post, db)

    async def get(self, _id: Any, db: AsyncSession) -> Optional[Post]:
        if not (post := await super().get(_id, db)):
            raise DoesNotExistException(_id, self.model)

        return post

    @staticmethod
    async def put_like_dislike(post: Post, user: User, db: AsyncSession) -> Post:
        """
        Лайк/дизлайк
        """
        results = await db.execute(
            select(AssociationPostLikes).where(
                Post.id == post.id,
                User.id == user.id,
            )
        )
        if obj := results.one_or_none():
            post.like_count -= 1
            await db.delete(obj[0])
        else:
            post.like_count += 1
            db.add(
                AssociationPostLikes(
                    user_id=user.id,
                    post_id=post.id,
                )
            )
        try:
            await db.commit()
        except Exception:
            await db.rollback()
            raise

        return post
