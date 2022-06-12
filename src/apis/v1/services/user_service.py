from src.apis.v1.models.practices_model import practices
from src.apis.v1.models.roles_model import roles
from src.apis.v1.models.sp_apps_model import SPAPPS
from src.apis.v1.models.user_role_model import idp_user_role
from src.apis.v1.services.roles_service import RolesService
from src.apis.v1.services.type_of_user_service import TypeOfUserService
from src.apis.v1.models.idp_user_types_model import idp_user_types
from src.apis.v1.models.idp_users_model import idp_users
from src.apis.v1.models.user_idp_sp_apps_model import idp_sp
from fastapi import status
class UserService():

    def __init__(self, db):
        self.db = db

    def create_internal_idp_user(self, **kwargs):
        try:
            type_of_user_id = TypeOfUserService(self.db).get_type_of_user_db(kwargs.get('type_of_user'))
            if type_of_user_id is None:
                return "No User Role Found", status.HTTP_404_NOT_FOUND

            internal_user_role_id = RolesService(self.db).get_internal_roles_selected_db(kwargs.get('internal_user_role'))
            if internal_user_role_id is None:
                return "No Internal User Role Found", status.HTTP_404_NOT_FOUND

            type_of_user_id = type_of_user_id.id
            create_user = idp_users(
                uuid=kwargs.get('uuid'),
                organization_id=kwargs.get('organization_id'),
                nhs_number=kwargs.get('nhs_number'),
                username=kwargs.get('username'),
                first_name=kwargs.get('first_name'),
                last_name=kwargs.get('last_name'),
                email=kwargs.get('email'),
                password_hash = kwargs.get('password_hash'),
                reset_password_token = kwargs.get('reset_password_token'),
                reset_password_token_expiry = kwargs.get('reset_password_token_expiry'),
                created_date=kwargs.get('created_date'),
                updated_date=kwargs.get('updated_date'),
                last_login_date=kwargs.get('last_login_date'),
                is_active=kwargs.get('is_active'),
                user_type_id=type_of_user_id,
            )

            self.db.add(create_user)
            self.db.commit()

            objects = []
            sps_object = kwargs.get('sps_object_list')
            for sp in sps_object:
                objects.append(idp_sp(
                    is_accessible=True,
                    idp_users_id = create_user.id,
                    sp_apps_id  = sp.id,

                ))

            self.db.bulk_save_objects(objects)
            self.db.commit()

            user_role_data = idp_user_role(
                idp_users_id=create_user.id,
                roles_id=internal_user_role_id.id,
            )
            self.db.add(user_role_data)
            self.db.commit()

            return "created idp user", status.HTTP_201_CREATED
        except Exception as e:
            print(e,"error")
            return "Error: {}".format(e), status.HTTP_500_INTERNAL_SERVER_ERROR
    
    def get_all_sps_practice_roles_db(self):
        try:
            practice_roles_data_object = self.db.query(SPAPPS).all()
            practice_roles_data = []
            for practice_role in practice_roles_data_object:
                practice_roles_data.append({
                    "id": practice_role.id,
                    "name":practice_role.name,
                    "sp_app_name": practice_role.display_name,
                    "sp_app_image": practice_role.logo_url,
                    "roles":[{"id":values.id,"name":values.label,"is_active":values.is_active} for values in practice_role.roles],
                    "practices":[{"id":values.id,"name":values.name}  for values in practice_role.practices]
                })

            return practice_roles_data, status.HTTP_200_OK
        except Exception as e:
            return "Error: {}".format(e), status.HTTP_500_INTERNAL_SERVER_ERROR
