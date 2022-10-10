
from src.apis.v1.models.practices_model import practices
from src.packages.dao.dao import DAO
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

def create_sp_apps_filter_query(filter_data):

    filter_query = practices.id != None
    for filter_key, filter_value in filter_data.items():
        filter_query = filter_query & (filter_key == filter_value)
    return filter_query

class SpsDAO(DAO):
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def get(self, filter_data:dict):
        filter_query = create_sp_apps_filter_query(filter_data)
        result = (await self.db.execute(select(practices).filter(filter_query))).scalars().unique().all()
        return result

    async def get_all(self):
        result = (await self.db.execute(select(practices))).scalars().unique().all()
        return result

    def update(self):
        pass

    def delete(self):
        pass

    def save(self):
        pass