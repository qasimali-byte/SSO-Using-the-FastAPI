from src.apis.v1.helpers.custom_exceptions import CustomException
from src.apis.v1.models.idp_users_model import idp_users
from src.apis.v1.models.sp_apps_model import SPAPPS
from fastapi import status
from src.apis.v1.models.user_idp_sp_apps_model import idp_sp


class UsersService():

    def __init__(self, db):
        self.db = db

    def get_users_info_db(self) -> list:
        try:
            users_info_object = self.db.query(idp_users, SPAPPS).join(idp_sp, idp_users.id == idp_sp.idp_users_id).join(SPAPPS, idp_sp.sp_apps_id == SPAPPS.id).all()
            user_data = {}
            for user, apps in users_info_object:
                if user_data.get(user.id) is None:
                    user_data[user.id] = dict({
                        "first_name": user.first_name,
                        "last_name": user.last_name,
                        "email": user.email,
                        "id": user.id,
                        "products":[]
                        })
                    user_data[user.id]["products"].append(apps.name)
                else:
                    user_data[user.id]["products"].append(apps.name)
            user_data = [values for values in user_data.values()]
            return user_data
        except Exception as e:
            raise CustomException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, message=str(e)+"- error occured in use_service.py")
