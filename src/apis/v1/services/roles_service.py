from src.apis.v1.models.roles_model import roles
from src.apis.v1.models.user_role_model import idp_user_role
from src.apis.v1.models.idp_users_model import idp_users
from src.apis.v1.models.idp_user_types_model import idp_user_types


class RolesService():
    def __init__(self, db) -> None:
        self.db = db

    def get_internal_roles_db(self):
        try:
            internal_roles_data_object = self.db.query(roles).join(idp_user_types).filter(idp_user_types.user_type == "internal").all()
            return internal_roles_data_object
            
        except Exception as e:
            print(e)
            return []
        