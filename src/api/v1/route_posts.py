from fastapi import APIRouter
from fastapi import (
    Depends,
    status,
)
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.background import BackgroundTasks

from api.deps import authorized_user
from api.exceptions import DoesNotExistException
from apps.users.models import User
from apps.users.auth.bearer import JWTBearer
from apps.posts.exceptions import (
    LikeOwnPostException,
    EditOwnPostException,
)
from apps.posts.models import Post
from apps.posts.services import PostServices
from apps.posts.schemas import (
    ShowPost,
    PostBase,
)
from core.cache import CacheBackend
from core.session import db

router = APIRouter()
cache = CacheBackend(Post)


@router.post(
    "/create",
    response_model=ShowPost,
    status_code=status.HTTP_201_CREATED,
)
async def create_post(
    post_schema: PostBase,
    back_task: BackgroundTasks,
    post_services: PostServices = Depends(),
    user: User = Depends(authorized_user),
    db: AsyncSession = Depends(db.get_db),
):
    post = await post_services.create_with_author(post_schema, user, db)
    back_task.add_task(cache.set_cache, ShowPost.from_orm(post), post.id)

    return post


@router.get(
    "/all",
    response_model=list[ShowPost],
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(JWTBearer())],
)
async def all_posts(
    post_services: PostServices = Depends(), db: AsyncSession = Depends(db.get_db)
):
    return await post_services.list(db)


@router.get(
    "/get/{id}",
    response_model=ShowPost,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(JWTBearer())],
)
async def get_post(
    _id: int,
    back_task: BackgroundTasks,
    post_services: PostServices = Depends(),
    db: AsyncSession = Depends(db.get_db),
):
    if not (post := await cache.get_cache(_id)):
        if post := await post_services.get(_id, db):
            back_task.add_task(cache.set_cache, ShowPost.from_orm(post), _id)
        else:
            raise DoesNotExistException(_id, Post)

    return post


@router.patch(
    "/update/{id}",
    status_code=status.HTTP_200_OK,
    response_model=ShowPost,
)
async def update_post(
    _id: int,
    back_task: BackgroundTasks,
    post_schema: PostBase,
    post_services: PostServices = Depends(),
    user: User = Depends(authorized_user),
    db: AsyncSession = Depends(db.get_db),
):
    if _id == user.id:
        if post := await post_services.update(_id, post_schema, db):
            back_task.add_task(cache.set_cache, ShowPost.from_orm(post), _id)
        else:
            raise DoesNotExistException(_id, Post)
    else:
        raise EditOwnPostException()

    return post


@router.delete("/delete/{id}")
async def delete_post(
    _id: int,
    back_task: BackgroundTasks,
    post_services: PostServices = Depends(),
    user: User = Depends(authorized_user),
    db: AsyncSession = Depends(db.get_db),
):
    if _id == user.id:
        if post_id := await post_services.delete(_id, db):
            back_task.add_task(cache.del_cache, post_id)
        else:
            raise DoesNotExistException(_id, Post)
    else:
        raise EditOwnPostException()

    return {"msg": f"Successfully deleted (Post_id={post_id})"}


@router.post(
    "/like/{id}",
    status_code=status.HTTP_200_OK,
    response_model=ShowPost,
)
async def like_post(
    _id: int,
    back_task: BackgroundTasks,
    post_services: PostServices = Depends(),
    user: User = Depends(authorized_user),
    db: AsyncSession = Depends(db.get_db),
):
    if post := await post_services.get(_id, db):
        if post.author is not user:
            post: Post = await post_services.put_like_dislike(post, user, db)
            back_task.add_task(cache.set_cache, ShowPost.from_orm(post), _id)
        else:
            raise LikeOwnPostException()
    else:
        raise DoesNotExistException(_id, Post)

    return post
