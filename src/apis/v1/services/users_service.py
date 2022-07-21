from sqlalchemy import and_
from src.apis.v1.helpers.custom_exceptions import CustomException
from src.apis.v1.models.idp_user_apps_roles_model import idp_user_apps_roles
from src.apis.v1.models.idp_users_model import idp_users
from src.apis.v1.models.roles_model import roles
from src.apis.v1.models.sp_apps_model import SPAPPS
from fastapi import status
from src.apis.v1.models.sp_apps_role_model import sp_apps_role
from src.apis.v1.models.user_idp_sp_apps_model import idp_sp
from sqlalchemy.sql import select

class UsersService():

    def __init__(self, db):
        self.db = db
        
    def get_external_users_info_db(self,user_type_id:int, page_limit:int, page_offset:int) -> tuple:
        try:
            count_records = self.db.query(idp_users.id).filter(idp_users.user_type_id == user_type_id).count()
            subquery = self.db.query(idp_users.id).filter(idp_users.user_type_id == user_type_id).order_by(idp_users.id.asc()).limit(page_limit).offset(page_offset*page_limit).subquery()
            users_info_object = self.db.query(idp_users,SPAPPS).order_by(idp_users.id.asc()).filter(idp_users.id.in_(select(subquery))) \
            .join(idp_sp, idp_users.id == idp_sp.idp_users_id,isouter=True).join(SPAPPS, idp_sp.sp_apps_id == SPAPPS.id,isouter=True).all()

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
                    if apps is not None:
                        user_data[user.id]["products"].append(apps.name)
                else:
                    if apps is not None:
                        user_data[user.id]["products"].append(apps.name)

            
            user_data = [values for values in user_data.values()]
            return user_data, count_records

        except Exception as e:
            raise CustomException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, message=str(e)+"- error occured in users_service.py")

    def get_internal_external_users_info_db(self,user_role:str, page_limit:int, page_offset:int) -> tuple:
        try:
            if user_role == "super-admin":

                subquery = self.db.query(idp_users.id) \
                .join(idp_user_apps_roles, idp_users.id == idp_user_apps_roles.idp_users_id, isouter=True) \
                .join(sp_apps_role, idp_user_apps_roles.sp_apps_role_id == sp_apps_role.id, isouter=True) \
                .join(roles, sp_apps_role.roles_id == roles.id, isouter=True) \
                .filter(roles.name != "super-admin") \
                .subquery()

                count_records = self.db.query(idp_users.id).filter(idp_users.id.in_(select(subquery))).count()

                subquery = self.db.query(idp_users.id) \
                .order_by(idp_users.id.asc()).filter(idp_users.id.in_(select(subquery))).limit(page_limit).offset(page_offset*page_limit).subquery()
                
            elif user_role == "sub-admin":

                subquery = self.db.query(idp_users.id) \
                .join(idp_user_apps_roles, idp_users.id == idp_user_apps_roles.idp_users_id, isouter=True) \
                .join(sp_apps_role, idp_user_apps_roles.sp_apps_role_id == sp_apps_role.id, isouter=True) \
                .join(roles, sp_apps_role.roles_id == roles.id) \
                .filter(and_(roles.name != "super-admin",roles.name != "sub-admin")) \
                .subquery()

                count_records = self.db.query(idp_users.id).filter(idp_users.id.in_(select(subquery))).count()

                subquery = self.db.query(idp_users.id) \
                .order_by(idp_users.id.asc()).filter(idp_users.id.in_(select(subquery))).limit(page_limit).offset(page_offset*page_limit).subquery()

            users_info_object = self.db.query(idp_users,SPAPPS).order_by(idp_users.id.asc()).filter(idp_users.id.in_(select(subquery))) \
            .join(idp_sp, idp_users.id == idp_sp.idp_users_id, isouter=True).join(SPAPPS, idp_sp.sp_apps_id == SPAPPS.id, isouter=True).all()

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
                    if apps is not None:
                        user_data[user.id]["products"].append(apps.name)
                else:
                    if apps is not None:
                        user_data[user.id]["products"].append(apps.name)

            
            user_data = [values for values in user_data.values()]
            return user_data, count_records
        except Exception as e:
            raise CustomException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, message=str(e)+"- error occured in users_service.py")