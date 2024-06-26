from typing import Union
from sqlalchemy import and_
from src.apis.v1.models.api_model import api
from src.apis.v1.models.driq_practices_role_model import driq_practices_role
from src.apis.v1.models.role_api_model import role_api

from src.apis.v1.models.sp_apps_role_driq_practice_role_model import sp_apps_role_driq_practice_role
from src.apis.v1.utils.roles_utils import format_loged_in_user_role, format_roles_with_selected_roles
from ..helpers.custom_exceptions import CustomException
from src.apis.v1.models.idp_user_apps_roles_model import idp_user_apps_roles
from src.apis.v1.models.sp_apps_model import SPAPPS
from src.apis.v1.models.sp_apps_role_model import sp_apps_role
from src.apis.v1.models.roles_model import roles
from src.apis.v1.models.type_role_permissions_model import type_role_permissions

from src.apis.v1.models.idp_users_model import idp_users
from src.apis.v1.models.idp_user_types_model import idp_user_types
from src.apis.v1.validators.roles_validator import  RolesValidator, SubRolesValidator
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
                dr_iq_practices_roles_object = self.db.query(sp_apps_role).filter(and_(sp_apps_role.roles_id == values.id, sp_apps_role.sp_apps_id == 3))\
                    .options(joinedload(sp_apps_role.driq_practices_role)).first()
                sub_roles = SubRolesValidator(id=values.id,name=values.label,dr_iq_role_id=values.dr_iq_role_id,sub_roles=dr_iq_practices_roles_object.driq_practices_role).dict()
                roles.append(sub_roles)
            return roles
        else:
            roles = RolesValidator(roles = roles_object.roles).dict()
            
            return roles["roles"]
        
        
    def get_apps_practice_roles_for_loged_in_user(self, sp_app_id):
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

    def get_user_selected_role(self, sp_app_name, user_id) -> str:
        try:
            ## This function is mainly used to get the role in ez-login application
            user_selected_role_object = self.db.query(idp_users.id,roles.name)\
            .filter(idp_users.id == user_id) \
            .join(idp_user_apps_roles, idp_user_apps_roles.idp_users_id == idp_users.id) \
            .join(sp_apps_role, sp_apps_role.id == idp_user_apps_roles.sp_apps_role_id) \
            .join(roles, roles.id == sp_apps_role.roles_id) \
            .join(SPAPPS, SPAPPS.id == sp_apps_role.sp_apps_id).filter(SPAPPS.name == sp_app_name) \
            .first()
            if user_selected_role_object:
                return user_selected_role_object[1]
            return 'external-user'
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
    
    def get_user_loged_in_ezlogin_roles(self, user_id):
        role_name = self.get_user_selected_role(sp_app_name="ez-login", user_id=user_id)
        if role_name == "super-admin":
            user_roles = {"id":15,"name":"Super Admin","sub_roles":None}
        elif role_name == "sub-admin":
            user_roles = {"id":1, "name":"Sub Admin","sub_roles":None}
        elif role_name == "practice-administrator":
            user_roles = {"id":16, "name":"Practice Admin","sub_roles":None}
        else:
            user_roles = {"id":17, "name":"External User","sub_roles":None}

        return user_roles

    def get_selected_roles_db_by_id(self, app_id, user_id, selected_userid):
        
        if app_id == 7:
            all_app_roles = self.get_ezlogin_roles(user_id=user_id)
        else:
            all_app_roles = self.get_apps_practice_roles(app_id)
        selected_roles = self.get_user_selected_role_db_appid_userid(app_id=app_id, selected_userid=selected_userid)

        all_app_roles = format_roles_with_selected_roles(all_app_roles, selected_roles)
        return all_app_roles

    def get_loged_in_user_selected_roles_db_by_id(self, app_id, user_id, selected_userid):
        
        if app_id == 7:
            all_app_roles = self.get_user_loged_in_ezlogin_roles(user_id=user_id)
        else:
            all_app_roles = self.get_user_selected_role_db_appid_userid(app_id=app_id, selected_userid=selected_userid)
            all_app_roles=format_loged_in_user_role(all_app_roles)            
        return all_app_roles



    def get_allowed_api_by_role(self, role_name, method, url):

        return self.db.query(roles).join(role_api, roles.id == role_api.role_id).join(api, role_api.api_id == api.id) \
            .filter(and_(roles.name == role_name,api.method == method, api.name == url,role_api.is_allowed == True)).first()

    def get_ezlogin_role_only(self, user_id):
        role_name = self.get_user_selected_role(sp_app_name="ez-login", user_id=user_id)
        ezlogin_role = []
        if role_name is not None:
            ezlogin_role.append(role_name)
            return ezlogin_role
        else:
            return ['external user']

    def create_role_api_db(self, role_api_data):
        try:
            create_role_api = role_api(**role_api_data)
            self.db.add(create_role_api)
            self.db.commit()
            return "successfully created a role_api", status.HTTP_201_CREATED
        except Exception as e:
            raise CustomException(str(e) + "error occurred in roles_service.py", status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete_role_api_db(self, role_api_id):
        try:
            role_api_res = self.db.query(role_api).filter(role_api.id == role_api_id).first()
            if role_api_res is not None:
                self.db.query(role_api).filter(role_api.id == role_api_id).delete()
                self.db.commit()
                return "successfully deleted role_api", status.HTTP_200_OK
            else:
                return "role_api_id not found", status.HTTP_404_NOT_FOUND
        except Exception as e:
            raise CustomException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                  message=str(e) + "- error occurred in roles_service.py")

    def create_role_db(self, roles_data):
        try:
            create_role = roles(**roles_data)
            self.db.add(create_role)
            self.db.commit()
            return "created a role", status.HTTP_201_CREATED
        except Exception as e:
            raise CustomException(str(e) + "error occurred in roles_service.py",
                                  status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete_role_db(self, roles_id):
        if roles_id in [1, 15, 16, 17]:
            return "Roles [1,15,16,17] can't be deleted", status.HTTP_406_NOT_ACCEPTABLE
        else:
            try:
                role_res = self.db.query(roles).filter(roles.id == roles_id).first()
                if role_res is not None:
                    # First deleting where this role is assigned
                    self.db.query(role_api).filter(role_api.role_id == roles_id).delete()
                    self.db.query(sp_apps_role).filter(sp_apps_role.roles_id == roles_id).delete()
                    self.db.query(type_role_permissions).filter(type_role_permissions.roles_id == roles_id).delete()
                    # Now deleting role
                    self.db.query(roles).filter(roles.id == roles_id).delete()
                    self.db.commit()
                    return "Role deleted successfully", status.HTTP_200_OK
                else:
                    return "Role_id not found", status.HTTP_404_NOT_FOUND
            except Exception as e:
                raise CustomException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                      message=str(e) + "- error occurred in roles_service.py")