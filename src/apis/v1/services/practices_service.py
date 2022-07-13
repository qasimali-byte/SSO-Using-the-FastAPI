from sqlalchemy import func, union_all
from src.apis.v1.models.practices_model import practices
from src.apis.v1.utils.practices_utils import format_practices_edit_user_data_selected_unselected
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

    def get_selected_unselected_practices_dbquery_by_appid_userid(self, app_id, user_id, selected_user_id):
        ### total practices of user_id
        practices_als = aliased(practices, name='practices_aliased')
        practices_of_userid = self.db.query(practices,practices_als).with_entities(practices.id.label('practices_id'),practices.name.label('practices_name'),practices_als.id.label('practices_als_id'),practices_als.name.label('practices_als_name')) \
        .options(Load(practices).load_only("id","name"))\
        .options(Load(practices_als).load_only("id","name"))\
        .join(practices_als, practices.practice_region_id == practices_als.id, isouter=True).filter(practices.sp_apps_id == app_id) \
        .join(idp_users_practices,practices.id == idp_users_practices.practices_id).filter(idp_users_practices.idp_users_id == user_id) \

        ### total practices of selected_user_id
        practices_als = aliased(practices, name='practices_aliased')
        practices_of_selecteduserid = self.db.query(practices,practices_als).with_entities(practices.id.label('practices_id'),practices.name.label('practices_name'),practices_als.id.label('practices_als_id'),practices_als.name.label('practices_als_name')).options(Load(practices).load_only("id","name"))\
        .options(Load(practices_als).load_only("id","name"))\
        .join(practices_als, practices.practice_region_id == practices_als.id, isouter=True).filter(practices.sp_apps_id == app_id) \
        .join(idp_users_practices,practices.id == idp_users_practices.practices_id).filter(idp_users_practices.idp_users_id == selected_user_id) \

        ## union of user practices and selected user practices
        union_set = union_all(practices_of_userid, practices_of_selecteduserid).alias()

        ## get the count of practices of user_id and selected_user_id
        selected_unselected_practices_data =  self.db.query(union_set) \
        .with_entities(union_set.c.practices_id,union_set.c.practices_name,union_set.c.practices_als_id,union_set.c.practices_als_name,func.count(union_set.c.practices_id)) \
        .group_by(union_set.c.practices_id,union_set.c.practices_name,union_set.c.practices_als_id,union_set.c.practices_als_name).all()
        
        return selected_unselected_practices_data

    def get_selected_practices_db_by_id(self, app_id, user_id, selected_user_id):

        selected_unselected_practices_data = self.get_selected_unselected_practices_dbquery_by_appid_userid(app_id, user_id, selected_user_id)
        edit_practices_list = format_practices_edit_user_data_selected_unselected(selected_unselected_practices_data)
        return edit_practices_list

