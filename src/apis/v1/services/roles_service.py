from sqlalchemy import and_
from src.apis.v1.models.driq_practices_role_model import driq_practices_role

from src.apis.v1.models.sp_apps_role_driq_practice_role_model import sp_apps_role_driq_practice_role
from src.apis.v1.utils.roles_utils import format_roles_with_selected_roles
from ..helpers.custom_exceptions import CustomException
from src.apis.v1.models.idp_user_apps_roles_model import idp_user_apps_roles
from src.apis.v1.models.sp_apps_model import SPAPPS
from src.apis.v1.models.sp_apps_role_model import sp_apps_role
from src.apis.v1.models.roles_model import roles
from src.apis.v1.models.idp_users_model import idp_users
from src.apis.v1.models.idp_user_types_model import idp_user_types
from src.apis.v1.validators.roles_validator import RolesValidator, SubRolesValidator
from sqlalchemy.orm import joinedload
from fastapi import status
class RolesService():
    def __init__(self, db) -> None:
        self.db = db

    def get_selected_role_id(self, app_id, role_id):
        selected_role_id = self.db.query(sp_apps_role).filter(and_(sp_apps_role.sp_apps_id == app_id, sp_apps_role.roles_id == role_id)).first()
        return selected_role_id.id

    def assign_roles_user_db(self, selected_data):
        try:
            objects = []
            for roles_data in selected_data:
                objects.append(idp_user_apps_roles(
                    idp_users_id = roles_data[0],
                    sp_apps_role_id  = roles_data[1],
                    sub_roles_id = roles_data[2]
                ))

            self.db.bulk_save_objects(objects)
            self.db.commit()
            return "assigned roles to user"
            
        except Exception as e:
            raise CustomException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, message=str(e)+"error occured in roles service")

    def get_internal_roles_db(self):
        try:
            internal_roles_data_object = self.db.query(roles).join(idp_user_types).filter(idp_user_types.user_type == "internal").all()
            return internal_roles_data_object
            
        except Exception as e:
            print(e)
            return []

    def get_internal_roles_selected_db(self, internal_user_role):
        try:
            internal_roles_data_object = self.db.query(roles).join(idp_user_types).filter(idp_user_types.user_type == "internal").\
            filter(roles.name == internal_user_role).first()
            return internal_roles_data_object
            
        except Exception as e:
            print(e)
            return None

    def get_external_roles_db(self):
        try:
            external_roles_data_object = self.db.query(roles).join(idp_user_types).filter(idp_user_types.user_type == "external").all()
            return external_roles_data_object
            
        except Exception as e:
            print(e)
            return []

    def get_apps_practice_roles(self, sp_app_id):
        roles = []
        roles_object = self.db.query(SPAPPS).options(joinedload(SPAPPS.roles)).filter(SPAPPS.id == sp_app_id).first()
        if sp_app_id == 3:
            for values in roles_object.roles:
                dr_iq_practices_roles_object = self.db.query(sp_apps_role).filter(and_(sp_apps_role.roles_id == values.id, sp_apps_role.sp_apps_id == 3)).options(joinedload(sp_apps_role.driq_practices_role)).first()
                sub_roles = SubRolesValidator(id=values.id,name=values.label,sub_roles=dr_iq_practices_roles_object.driq_practices_role).dict()
                roles.append(sub_roles)

            return roles
        else:
            roles = RolesValidator(roles = roles_object.roles).dict()
            return roles["roles"]

    def get_user_selected_role(self, sp_app_name, user_id):
        try:
            user_selected_roles = []
            user_selected_role_object = self.db.query(idp_users,roles)\
            .filter(idp_users.id == user_id) \
            .join(idp_user_apps_roles, idp_user_apps_roles.idp_users_id == idp_users.id) \
            .join(sp_apps_role, sp_apps_role.id == idp_user_apps_roles.sp_apps_role_id) \
            .join(roles, roles.id == sp_apps_role.roles_id) \
            .all()

            for users_values,roles_values in user_selected_role_object:
                user_selected_roles.append(roles_values.name)

            if sp_app_name == "ez-login":
                return user_selected_roles[0]
            
            return user_selected_roles
        except Exception as e:
            raise CustomException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, message=str(e)+" - error occured in roles service")

    def get_user_selected_role_db_appid_userid(self, app_id, selected_userid):

        selected_roles = self.db.query(idp_user_apps_roles, roles, driq_practices_role) \
        .join(sp_apps_role, sp_apps_role.id == idp_user_apps_roles.sp_apps_role_id) \
        .join(roles, roles.id == sp_apps_role.roles_id) \
        .join(driq_practices_role,driq_practices_role.id == idp_user_apps_roles.sub_roles_id , isouter=True) \
        .filter(and_(idp_user_apps_roles.idp_users_id == selected_userid, sp_apps_role.sp_apps_id == app_id)) \
        .first()

        return selected_roles
    
    def get_ezlogin_roles(self, user_id):
        role_name = self.get_user_selected_role(sp_app_name="ez-login", user_id=user_id)
        if role_name == "super-admin":
            user_roles = [{"id":1,"name":"Sub Admin","sub_roles":[]}, {"id":16, "name":"Practice Admin","sub_roles":[]}]
        elif role_name == "sub-admin":
            user_roles = [{"id":16, "name":"Practice Admin","sub_roles":[]}]
        else:
            user_roles = []

        return user_roles

    def get_selected_roles_db_by_id(self, app_id, user_id, selected_userid):
        
        if app_id == 7:
            all_app_roles = self.get_ezlogin_roles(user_id=user_id)
        else:
            all_app_roles = self.get_apps_practice_roles(app_id)

        selected_roles = self.get_user_selected_role_db_appid_userid(app_id=app_id, selected_userid=selected_userid)

        all_app_roles = format_roles_with_selected_roles(all_app_roles, selected_roles)
        return all_app_roles
