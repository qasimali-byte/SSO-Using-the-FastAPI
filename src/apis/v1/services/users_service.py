from itertools import count
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
from src.apis.v1.utils.users_utils import get_order_by_query,get_subquery


class UsersService():

    def __init__(self, db):
        self.db = db
    

    def get_external_users_info_db(self,user_type_id:int, page_limit:int, page_offset:int,order_by:str,latest:bool,search:str,user_status:bool,\
        
        select_practices:str) -> tuple:

        try:
            get_order_by= get_order_by_query(order_by,latest)

            sub_query=get_subquery(search,select_practices,user_status)


            subquery_2 = self.db.query(idp_users.id).filter(and_(idp_users.user_type_id == user_type_id,idp_users.is_approved == True,*sub_query))\
                .subquery()

            count_records=self.db.query(idp_users.id).filter(idp_users.id.in_(select(subquery_2))).count()

            subquery_3=self.db.query(idp_users.id).filter(idp_users.id.in_(select(subquery_2))).limit(page_limit).offset(page_offset*page_limit).subquery()

            users_info_object=self.db.query(idp_users,SPAPPS).order_by(get_order_by).filter(idp_users.id.in_(select(subquery_3))).\
                join(idp_sp, idp_users.id == idp_sp.idp_users_id).\
                join(SPAPPS, idp_sp.sp_apps_id == SPAPPS.id).all()

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

    def get_internal_external_users_info_db(self,user_role:str, page_limit:int, page_offset:int,order_by:str,latest:bool,search:str,user_status:bool,\
        select_practices:str) -> tuple:
        try:
            get_order_by= get_order_by_query(order_by,latest)
            if user_role == "super-admin":
                subquery_1=self.db.query(idp_users.id)\
                .join(idp_user_apps_roles, idp_users.id == idp_user_apps_roles.idp_users_id) \
                .join(sp_apps_role, idp_user_apps_roles.sp_apps_role_id == sp_apps_role.id) \
                .join(roles, sp_apps_role.roles_id == roles.id) \
                .filter(roles.name == "super-admin").subquery()

            elif user_role == "sub-admin":
                subquery_1=self.db.query(idp_users.id)\
                .join(idp_user_apps_roles, idp_users.id == idp_user_apps_roles.idp_users_id) \
                .join(sp_apps_role, idp_user_apps_roles.sp_apps_role_id == sp_apps_role.id) \
                .join(roles, sp_apps_role.roles_id == roles.id) \
                .filter(roles.name == "sub-admin").subquery()
                

            sub_query=get_subquery(search,select_practices,user_status)

            subquery_2=self.db.query(idp_users.id).order_by(get_order_by)\
            .join(idp_user_apps_roles,idp_users.id == idp_user_apps_roles.idp_users_id )\
            .join(sp_apps_role, idp_user_apps_roles.sp_apps_role_id == sp_apps_role.id)\
            .join(SPAPPS,SPAPPS.id == sp_apps_role.sp_apps_id)\
            .filter(and_(idp_users.id.not_in(select(subquery_1)),idp_users.is_approved == True,*sub_query)).group_by(idp_users.id).subquery()

            subquery_3=self.db.query(idp_users.id).filter(idp_users.id.in_(select(subquery_2))).limit(page_limit).offset(page_offset*page_limit).subquery()

            count_records=self.db.query(idp_users.id).filter(idp_users.id.in_(select(subquery_2))).count()

            users_info_object=self.db.query(idp_users,SPAPPS).order_by(get_order_by).filter(idp_users.id.in_(select(subquery_3))) \
            .join(idp_sp, idp_users.id == idp_sp.idp_users_id).join(SPAPPS, idp_sp.sp_apps_id == SPAPPS.id).all()
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
