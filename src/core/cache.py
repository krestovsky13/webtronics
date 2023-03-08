import json
import re
from datetime import datetime
from typing import (
    TypeVar,
    Type,
    Optional,
)

from aioredis import Redis
from pydantic import BaseModel as PydanticModel
from pydantic.json import pydantic_encoder

from core.config import settings
from db.models import BaseModel

Model = TypeVar("Model", bound=BaseModel)
SchemaModel = TypeVar("SchemaModel", bound=PydanticModel)


class CacheBackend:
    """
    Класс кеширования данных
    """

    def __init__(self, model: Optional[Type[Model]] = None):
        self.redis: Redis = Redis(
            host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0
        )
        self.key = model

    def cache_key(self, uid: str | int) -> str:
        """
        Уникальный кэш-ключ
        """
        return f"{self.key.__tablename__}:{uid}" if self.key else uid

    async def set_cache(
        self, data: SchemaModel | dict, uid: str | int, expire: int = 60
    ):
        """
        Сериализация и сохранение хэша со сроком жизни
        """

        def serialize_dates(v):
            return v.strftime("%Y-%d-%m") if isinstance(v, datetime) else str(v)

        serializer = serialize_dates if isinstance(data, dict) else pydantic_encoder

        await self.redis.set(
            name=self.cache_key(uid),
            value=json.dumps(data, separators=(",", ":"), default=serializer),
            ex=expire,
        )

    async def get_cache(self, uid: str | int) -> dict:
        """
        Десериализация и получения хэша
        """

        def datetime_parser(dct: dict):
            for k, v in dct.items():
                if re.search(r"(\d{4}-\d{2}-\d{2})", str(v)):
                    try:
                        dct[k]: datetime.date = datetime.strptime(v, "%Y-%d-%m")
                    except:
                        pass
            return dct

        cache_key: str = self.cache_key(uid)
        data: bytes | str = await self.redis.get(cache_key)

        if data:
            return json.loads(data, object_hook=datetime_parser)

    async def del_cache(self, uid: str | int):
        cache_key: str = self.cache_key(uid)

        await self.redis.delete(cache_key)
