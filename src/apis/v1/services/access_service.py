from sqlalchemy import and_, or_
from src.apis.v1.helpers.custom_exceptions import CustomException
from src.apis.v1.models.idp_user_apps_roles_model import idp_user_apps_roles
from src.apis.v1.models.idp_users_model import idp_users
from src.apis.v1.models.roles_model import roles
from src.apis.v1.models.sp_apps_model import SPAPPS
from fastapi import status, HTTPException
from src.apis.v1.models.sp_apps_role_model import sp_apps_role
from src.apis.v1.models.user_idp_sp_apps_model import idp_sp


class AccessService():

    def __init__(self, db):
        self.db = db

    def is_valid_email(self, user_email):
        return True if self.db.query(idp_users, SPAPPS).filter(
            idp_users.email == user_email) is not None else False

    def get_user_apps_info_db(self, user_email) -> dict:
        users_info_object = self.db.query(idp_users, SPAPPS).filter(
        idp_users.email==user_email). \
        join(idp_sp, idp_users.id == idp_sp.idp_users_id). \
        join(SPAPPS, idp_sp.sp_apps_id == SPAPPS.id).all()

        if users_info_object:
            products = dict({"products":[]})
            products.update({"user": users_info_object[0][0]})
            for user, apps in users_info_object:
                products["products"].append(
                        dict({
                        "email": user.email,
                        "product_name": apps.display_name,
                        "logo": apps.logo_url,
                        "product_id": apps.id
                     })
                )
            return products
        else:
            raise CustomException(status_code=status.HTTP_404_NOT_FOUND, message='No data found for this user')





    def get_user_info_db(self, user_email) -> dict:

        try:
            users_info_object = self.db.query(idp_users).filter(
            idp_users.email==user_email)
            return users_info_object

        except Exception as e:
            raise CustomException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                  message=str(e) + "- error occured in users_service.py")