from src.apis.v1.helpers.customize_response import custom_response
from src.apis.v1.services.roles_service import RolesService
from src.apis.v1.validators.common_validators import ErrorResponseValidator
from fastapi import status
from src.apis.v1.validators.roles_validator import InternalRoleValidatorOut

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