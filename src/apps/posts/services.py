from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.repository import BaseRepository
from apps.posts.models import Post, AssociationPostLikes
from apps.posts.schemas import PostCreate, PostBase
from apps.users.models import User


class PostServices(BaseRepository[Post, PostCreate, PostBase]):
    """
    Класс операций с постами
    """

    def __init__(self):
        super().__init__(Post)

    async def create_with_author(
        self, post: PostBase, user: User, db: AsyncSession
    ) -> Post:
        post = PostCreate(**post.dict(), author_id=user.id)

        return await super().create(post, db)

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
