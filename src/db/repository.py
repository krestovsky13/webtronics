from typing import (
    Any,
    Generic,
    Optional,
    Type,
    TypeVar,
)

from pydantic import BaseModel as SchemaModel

from sqlalchemy import update as sqlalchemy_update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from db.models import BaseModel


Model = TypeVar("Model", bound=BaseModel)
CreateSchema = TypeVar("CreateSchema", bound=SchemaModel)
UpdateSchema = TypeVar("UpdateSchema", bound=SchemaModel)


class BaseRepository(Generic[Model, CreateSchema, UpdateSchema]):
    """
    Базовый CRUD моделей для api
    """

    def __init__(self, model: Type[Model]):
        self.model = model

    async def create(self, obj: Type[Model] | CreateSchema, db: AsyncSession) -> Model:
        """
        Создание нового объекта модели
        """
        # Для возможности ручного создания не по схеме
        if isinstance(obj, BaseModel):
            db.add(obj)
        else:
            obj = self.model(**obj.dict())
            db.add(obj)
        try:
            await db.commit()
        except Exception:
            await db.rollback()
            raise

        return obj

    async def list(self, db: AsyncSession) -> Optional[list[Model]]:
        """
        Список всех объектов модели
        """
        result = await db.execute(select(self.model))

        return result.scalars().all()

    async def get(self, _id: Any, db: AsyncSession) -> Optional[Model]:
        """
        Получить объект модели по id
        """
        results = await db.execute(select(self.model).where(self.model.id == _id))
        if obj := results.one_or_none():
            return obj[0]

    async def update(
        self, _id: Any, obj: UpdateSchema, db: AsyncSession
    ) -> Optional[Model]:
        """
        Обновить объект модели по id
        """
        query = (
            sqlalchemy_update(self.model)
            .where(self.model.id == _id)
            .values(**obj.dict())
        )
        results = await db.execute(query)
        if results.rowcount:
            try:
                await db.commit()
            except Exception:
                await db.rollback()
                raise

            return await self.get(_id, db)

    async def delete(self, _id: Any, db: AsyncSession) -> int:
        """
        Удаление объекта модели по id
        """
        if obj := await self.get(_id, db):
            await db.delete(obj)
            await db.commit()

            return _id
