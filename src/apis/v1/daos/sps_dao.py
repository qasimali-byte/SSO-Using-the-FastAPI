
from src.apis.v1.models.sp_apps_model import SPAPPS
from src.packages.dao.dao import DAO
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

def create_sp_apps_filter_query(filter_data):

    filter_query = SPAPPS.id != None
    for filter_key, filter_value in filter_data.items():
        filter_query = filter_query & (filter_key == filter_value)
    return filter_query

class SyncSpsDAO(DAO):
    def __init__(self, db) -> None:
        self.db = db

    def get(self, filter_data:dict):
        filter_query = create_sp_apps_filter_query(filter_data)
        result = self.db.query(SPAPPS).filter(filter_query).all()
        return result

    async def get_all(self):
        result = self.db.query(SPAPPS).all()
        return result

    def update(self):
        pass

    def delete(self):
        pass

    def save(self):
        pass 
class SpsDAO(DAO):
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def get(self, filter_data:dict):
        filter_query = create_sp_apps_filter_query(filter_data)
        result = (await self.db.execute(select(SPAPPS).filter(filter_query))).scalars().unique().all()
        return result

    async def get_all(self):
        result = (await self.db.execute(select(SPAPPS))).scalars().unique().all()
        return result

    def update(self):
        pass

    def delete(self):
        pass

    def save(self):
        pass