from src.apis.v1.models.practices_model import practices
from src.apis.v1.utils.practices_utils import format_practices_edit_user_data
from ..helpers.custom_exceptions import CustomException
from src.apis.v1.models.idp_users_practices_model import idp_users_practices
from fastapi import status
from sqlalchemy.orm import aliased, load_only,Load

class PracticesService():
    def __init__(self, db):
        self.db = db

    def assign_practices_user_db(self, user_id, practices_list):
        try:
            objects = []
            sps_practices = practices_list

            for practice in sps_practices:
                objects.append(idp_users_practices(
                    idp_users_id = user_id,
                    practices_id  = practice,
                ))

            self.db.bulk_save_objects(objects)
            self.db.commit()
            return "assigned practices to user"

        except Exception as e:
            raise CustomException(message=str(e) + "error occured in practices service", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def get_practices_db_by_appid_userid(self, app_id, user_id):

        practices_als = aliased(practices, name='practices_aliased')
        practices_of_userid = self.db.query(practices,practices_als).options(Load(practices).load_only("id","name"))\
        .options(Load(practices_als).load_only("id","name"))\
        .join(practices_als, practices.practice_region_id == practices_als.id, isouter=True).filter(practices.sp_apps_id == app_id) \
        .join(idp_users_practices,practices.id == idp_users_practices.practices_id).filter(idp_users_practices.idp_users_id == user_id) \
        .all()

        return practices_of_userid

    def get_selected_practices_db_by_id(self, app_id, user_id, selected_user_id):

        practices_of_userid = self.get_practices_db_by_appid_userid(app_id, user_id)
        practices_of_selected_user_id = self.get_practices_db_by_appid_userid(app_id, selected_user_id)
        regions_list = format_practices_edit_user_data(practices_of_userid, practices_of_selected_user_id)
        return regions_list

