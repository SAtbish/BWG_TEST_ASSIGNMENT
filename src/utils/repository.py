from abc import ABC, abstractmethod

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_pagination.paginator import paginate


def get_filters_string(
        tablename: str,
        filters: dict = None,
        order_by: str = None,
        order_direction: str = None,
        limit: int = None
):
    if filters is None:
        filters = {}
    stmt = f"SELECT * FROM {tablename} "
    if filters:
        stmt += "WHERE "
        for key, value in filters.items():
            stmt += f"{key} = {repr(value) if isinstance(value, str) else value} AND "
        stmt = stmt[:-4]
    if order_by:
        stmt += f"ORDER BY {order_by} {order_direction} "
    if limit:
        stmt += f"LIMIT {limit}"
    stmt += ";"
    return text(stmt)


class AbstractRepository(ABC):
    @abstractmethod
    async def create_one(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def read_last(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def get_all(self, *args, **kwargs):
        raise NotImplementedError


class SQLAlchemyRepository(AbstractRepository):
    model = None

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_one(self, data: dict):
        keys = str(tuple(data.keys())).replace("'", "")
        values = str(tuple(data.values()))
        stmt = text(f"INSERT INTO {self.model.__tablename__} {keys} VALUES {values};")
        await self.session.execute(stmt)

    async def create_many(self, data: list[dict]):
        if data:
            keys = str(tuple(data[0].keys())).replace("'", "")
            values = str([str(tuple(elem.values())) for elem in data]).translate({ord(x): '' for x in ['"', "[", "]"]})
            stmt = text(f"INSERT INTO {self.model.__tablename__} {keys} VALUES {values};")
            await self.session.execute(stmt)
        else:
            raise ValueError("nothing to add")

    async def read_last(self, **filters):
        stmt = get_filters_string(
            tablename=self.model.__tablename__,
            filters=filters,
            order_by="id",
            order_direction="DESC",
            limit=1
        )
        objects = await self.session.execute(stmt)
        obj = objects.first()
        if obj:
            obj = self.model.to_read_model(*obj)
            return obj, None

        return obj, "not_find"

    async def read_one(self, **filters):
        stmt = get_filters_string(
            tablename=self.model.__tablename__,
            filters=filters
        )
        objects = await self.session.execute(stmt)

        obj = objects.first()
        if obj:
            obj = self.model.to_read_model(*obj)
            return obj, None

        return obj, "not_find"

    async def get_all(self, **filters):
        stmt = get_filters_string(
            tablename=self.model.__tablename__,
            filters=filters
        )
        objects = await self.session.execute(stmt)
        result = [self.model.to_read_model(*obj) for obj in objects.all()]
        return result, None

    async def get_all_paginated(self, **filters):
        stmt = get_filters_string(
            tablename=self.model.__tablename__,
            filters=filters
        )
        objects = await self.session.execute(stmt)
        paginated_objects = paginate(sequence=[self.model.to_read_model(*obj) for obj in objects.all()])
        return paginated_objects
