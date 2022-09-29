
from src.apis.v1.daos.sps_dao import SpsDAO
from sqlalchemy.ext.asyncio import AsyncSession

from src.apis.v1.models.sp_apps_model import SPAPPS
from src.apis.v1.validators.sps_validator import ListSpAppsGeneralValidator

class AsyncSpsController():
    def __init__(self, db:AsyncSession) -> None:
        self.db = db

    async def get_all_sps_product(self):
        dto = await SpsDAO(self.db).get(filter_data={SPAPPS.is_active: True})
        return ListSpAppsGeneralValidator.from_orm(dto).dict()
        