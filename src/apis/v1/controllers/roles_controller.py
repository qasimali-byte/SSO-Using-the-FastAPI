from ..helpers.custom_exceptions import CustomException
from src.apis.v1.helpers.customize_response import custom_response
from src.apis.v1.services.roles_service import RolesService
from src.apis.v1.validators.common_validators import ErrorResponseValidator
from fastapi import status
from src.apis.v1.validators.roles_validator import InternalRoleValidatorOut, RoleAPIDeleteValidatorOut

class RolesController():
    def __init__(self, db):
        self.db = db

    def internal_roles(self):
        try:
            data = RolesService(self.db).get_internal_roles_db()
            if data:
                    internal_roles_data = [{"id":values.id,"name":values.name,"label":values.label,"is_active":values.is_active,"type_of_user":"internal"} for values in data]
                    validated_response = InternalRoleValidatorOut(roles=internal_roles_data)
                    response = custom_response(data=validated_response,status_code=status.HTTP_200_OK)
                    return response
            else:
                validated_response = []
                response = custom_response(data=validated_response,status_code=status.HTTP_200_OK)
                return response


        except Exception as e:
            data = ErrorResponseValidator(message=str(e),status=False)
            response = custom_response(data=data,status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
            return response

    def external_roles(self):
        try:
            data = RolesService(self.db).get_external_roles_db()
            if data:
                    internal_roles_data = [{"id":values.id,"name":values.name,"label":values.label,"is_active":values.is_active,
                    "type_of_user":"external"} for values in data]
                    validated_response = InternalRoleValidatorOut(roles=internal_roles_data)
                    response = custom_response(data=validated_response,status_code=status.HTTP_200_OK)
                    return response
            else:
                validated_response = []
                response = custom_response(data=validated_response,status_code=status.HTTP_200_OK)
                return response


        except Exception as e:
            data = ErrorResponseValidator(message=str(e),status=False)
            response = custom_response(data=data,status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
            return response

    def get_selected_role_id(self, app_id, role_id):
         return RolesService(self.db).get_selected_role_id(app_id=app_id, role_id=role_id)

    def assign_roles_to_user(self,user_id, roles_list):
        
        selected_role_id = []
        for role in roles_list:
            try:
                selected_role_id.append(tuple([user_id,self.get_selected_role_id(app_id=role[0], role_id=role[1]),role[2]]))
            except Exception as e:
                raise CustomException(message=str(e) + "error occured in roles controller", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

        roles_data = RolesService(self.db).assign_roles_user_db(selected_data= selected_role_id)
        return roles_data

    def get_allowed_roles_by_userid(self, app_id, user_id, selected_id):

        roles_object = RolesService(self.db)
        selected_roles_list = roles_object.get_selected_roles_db_by_id(app_id, user_id, selected_id)
        return selected_roles_list
    

    def get_allowed_roles_by_userid_loged_in_user(self, app_id, user_id, selected_id):

        roles_object = RolesService(self.db)
        selected_roles_list = roles_object.get_loged_in_user_selected_roles_db_by_id(app_id, user_id, selected_id)
        return selected_roles_list

    def get_ezlogin_user_role(self, user_id):
        return RolesService(self.db).get_user_selected_role("ez-login", user_id)

    def get_allowed_api_by_role(self, role_name, method, url) -> bool:
        allowed_role = RolesService(self.db).get_allowed_api_by_role(role_name, method, url)
        if allowed_role:
            return True
        else:
            return False

    def get_roles_by_app_id(self, app_id):
        return RolesService(self.db).get_apps_practice_roles(app_id)

    def create_role_api(self, role_api_data):
        message, status_code = RolesService(self.db).create_role_api_db(role_api_data)
        response = custom_response(data=message, status_code=status_code)
        return response

    def delete_role_api(self, role_api_id):

        message, status_code = RolesService(self.db).delete_role_api_db(role_api_id)
        response = custom_response(data=message, status_code=status_code)
        return response

    def create_role(self, roles_data):
        message, status_code = RolesService(self.db).create_role_db(roles_data)
        response = custom_response(data=message, status_code=status_code)
        return response

    def delete_role(self, roles_id):

        message, status_code = RolesService(self.db).delete_role_db(roles_id)
        response = custom_response(data=message, status_code=status_code)
        return response
