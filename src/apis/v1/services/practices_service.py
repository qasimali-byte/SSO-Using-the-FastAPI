from sqlalchemy import func, or_
from src.apis.v1.models.practice_regions_model import practice_regions
from src.apis.v1.models.practices_model import practices
from src.apis.v1.utils.practices_utils import  format_practices_edit_user_data_selected_unselected, format_practices_user_data_selected
from src.apis.v1.models.sp_apps_model import SPAPPS
from ..helpers.custom_exceptions import CustomException
from src.apis.v1.models.idp_users_practices_model import idp_users_practices
from fastapi import status
from sqlalchemy.orm import aliased, load_only,Load

class PracticesService():
    def __init__(self, db):
        self.db = db

    def assign_practices_user_db(self, user_id, practices_list, practices_dr_iq_region_list=None):
        try:
            objects = []
            for index, practice in enumerate(practices_list):
                region_id = None
                if practices_dr_iq_region_list and len(practices_dr_iq_region_list) > index:
                    region_id = int(practices_dr_iq_region_list[index])
                
                if region_id != practice:
                    objects.append(idp_users_practices(
                        idp_users_id=user_id,
                        practices_id=practice,
                        dr_iq_practice_region_id=region_id
                    ))

            if objects:
                self.db.bulk_save_objects(objects)
                self.db.commit()

            return "Assigned practices to user"
        except Exception as e:
            raise CustomException(message=str(e) + " Error occurred in practices service",
                                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)





    def get_practices_db_by_app_name(self, app_name):
        
        region_id_label = practices.region_id.label('region_id') if app_name == 'driq' else practices.practice_region_id.label('region_id')

        practices_of_app = self.db.query(
            practices.id,
            practices.name,
            region_id_label
        ).join(
            SPAPPS, SPAPPS.id == practices.sp_apps_id
        ).filter(
            SPAPPS.sp_metadata == app_name
        ).all()


        return practices_of_app


    def get_practices_db_by_appid_userid(self, app_id, user_id):

        practices_als = aliased(practices, name='practices_aliased')
        practices_of_userid = self.db.query(practices,practices_als).options(Load(practices).load_only("id","name"))\
        .options(Load(practices_als).load_only("id","name"))\
        .join(practices_als, practices.practice_region_id == practices_als.id, isouter=True).filter(practices.sp_apps_id == app_id) \
        .join(idp_users_practices,practices.id == idp_users_practices.practices_id).filter(idp_users_practices.idp_users_id == user_id) \
        .all()

        return practices_of_userid

    
    def get_selected_unselected_practices_dbquery_by_appid_userid(self, app_id, user_id, selected_user_id):
        
        if (app_id==3):
            selected_unselected_practices_data = self.db.query(
            practices.id.label('practices_id'),
            practices.name.label('practices_name'),
            practice_regions.id.label('practices_als_id'),
            practice_regions.name.label('practices_als_name'),
            func.count(practices.id)
            ).join(idp_users_practices, practices.id == idp_users_practices.practices_id)\
            .join(practice_regions, practices.region_id == practice_regions.id, isouter=True)\
            .filter(practices.sp_apps_id == app_id)\
            .filter(or_(idp_users_practices.idp_users_id == user_id, idp_users_practices.idp_users_id == selected_user_id))\
            .group_by(
                practices.id,
                practices.name,
                practice_regions.id,
                practice_regions.name
            ).all()
            
            
        else:
            practices_als = aliased(practices, name='practices_aliased')

            selected_unselected_practices_data = self.db.query(
                practices.id.label('practices_id'),
                practices.name.label('practices_name'),
                practices_als.id.label('practices_als_id'),
                practices_als.name.label('practices_als_name'),
                func.count(practices.id)
            ).join(idp_users_practices, practices.id == idp_users_practices.practices_id)\
            .join(practices_als, practices.practice_region_id == practices_als.id, isouter=True)\
            .filter(practices.sp_apps_id == app_id)\
            .filter(or_(idp_users_practices.idp_users_id == user_id, idp_users_practices.idp_users_id == selected_user_id))\
            .group_by(
                practices.id,
                practices.name,
                practices_als.id,
                practices_als.name
            ).all()
            
        return selected_unselected_practices_data
    
        


    def get_selected_practices_db_by_id(self, app_id, user_id, selected_user_id):
        selected_unselected_practices_data = self.get_selected_unselected_practices_dbquery_by_appid_userid(app_id, user_id, selected_user_id)
        edit_practices_list = format_practices_edit_user_data_selected_unselected(selected_unselected_practices_data,app_id)
        return edit_practices_list

    def get_selected_practices_db_by_id_loged_in_user(self, app_id, user_id, selected_user_id):
        
        if(app_id==3):
            subquery = self.db.query(idp_users_practices.practices_id) \
                .filter(idp_users_practices.idp_users_id == selected_user_id) \
                .subquery()

            data = self.db.query(practices) \
                .join(practice_regions, practices.region_id == practice_regions.id) \
                .filter(practices.sp_apps_id == 3) \
                .filter(practices.id.in_(self.db.query(subquery.c.practices_id))) \
                .with_entities(practices.id.label('practices_id'),
                            practices.name.label('practices_name'),
                            practice_regions.name.label('region_name'),
                            practice_regions.id.label('region_id'),
                            practices.dr_iq_practice_id) \
                .all()

            formatted_data = []
            region_dict = {}
            practices_list = []

            for practice in data:
                practice_id = practice.practices_id
                practice_name = practice.practices_name
                region_name = practice.region_name
                region_id = practice.region_id

                if region_id not in region_dict:
                    region_dict[region_id] = {'id': region_id, 'name': region_name, 'practices': []}
                region_dict[region_id]['practices'].append({'id': practice_id, 'name': practice_name})

            formatted_data = [region for region in region_dict.values()]
            return formatted_data

                
        else:
                    
            practices_als = aliased(practices, name='practices_aliased')
            practices_of_selecteduserid = self.db.query(practices,practices_als).with_entities(practices.id.label('practices_id'),practices.name.label('practices_name'),practices_als.id.label('practices_als_id'),practices_als.name.label('practices_als_name')).options(Load(practices).load_only("id","name"))\
            .options(Load(practices_als).load_only("id","name"))\
            .join(practices_als, practices.practice_region_id == practices_als.id, isouter=True).filter(practices.sp_apps_id == app_id) \
            .join(idp_users_practices,practices.id == idp_users_practices.practices_id).filter(idp_users_practices.idp_users_id == selected_user_id).all()
            formated_practices=format_practices_user_data_selected(practices_of_selecteduserid)
            return formated_practices

    def create_practice_db(self, practice_data):
        try:
            create_practice = practices(**practice_data)
            self.db.add(create_practice)
            self.db.commit()
            return "successfully created practice", status.HTTP_201_CREATED
        except Exception as e:
            raise CustomException(str(e) + "error occurred in practice service", status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete_practice_db(self, practice_id):
        try:
            practice = self.db.query(practices).filter(practices.id == practice_id).first()
            if practice is not None:
                self.db.query(idp_users_practices).filter(idp_users_practices.practices_id == practice_id).delete()
                self.db.query(practices).filter(practices.id == practice_id).delete()
                self.db.commit()
                return "Practice deleted successfully", status.HTTP_200_OK
            else:
                return "Practice not found", status.HTTP_404_NOT_FOUND
        except Exception as e:
            raise CustomException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                  message=str(e) + "- error occurred in practices_service.py")
    

