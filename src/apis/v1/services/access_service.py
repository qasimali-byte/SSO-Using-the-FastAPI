from sqlalchemy import and_, or_
from src.apis.v1.helpers.custom_exceptions import CustomException
from src.apis.v1.models.idp_user_apps_roles_model import idp_user_apps_roles
from src.apis.v1.models.idp_users_model import idp_users
from src.apis.v1.models.roles_model import roles
from src.apis.v1.models.sp_apps_model import SPAPPS
from fastapi import status, HTTPException
from src.apis.v1.models.sp_apps_role_model import sp_apps_role
from src.apis.v1.models.user_idp_sp_apps_model import idp_sp
from src.apis.v1.models.two_factor_authentication_model import two_factor_authentication

class AccessService():

    def __init__(self, db):
        self.db = db

    def is_valid_email(self, user_email):
        return True if self.db.query(idp_users, SPAPPS).filter(
            idp_users.email == user_email).first() is not None else False

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

    def if_user_exists_db(self, user_email) -> bool:

        # self.db.query(idp_users).filter(idp_users.email == user_email).first()
        return True if self.db.query(idp_users).filter(
            idp_users.email == user_email).first() is not None else False

    def get_contact_no_by_email(self, user_email) -> str:
        row = self.db.query(idp_users).filter(idp_users.email == user_email).one_or_none()
        if row:
            return row.contact_no if row.contact_no else ""
        raise CustomException(status_code=status.HTTP_404_NOT_FOUND, message='user email not found')

    def get_two_factor_authentication_cookie(self, user_id, phone_cookie) -> bool:
        res = self.db.query(two_factor_authentication).filter(two_factor_authentication.user_id == user_id).one_or_none()
        if res:
            cookie_id_db = str(res.cookie_id)
            if cookie_id_db == phone_cookie:
                return True
            else:
                return False
        return False

    def save_contact_no_db(self, email, contact_no):
        try:
            self.db.query(idp_users).filter(idp_users.email == email).update({idp_users.contact_no: contact_no})
            self.db.commit()
        except Exception as err:
            raise ValueError(err)

