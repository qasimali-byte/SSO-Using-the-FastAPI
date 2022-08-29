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
from src.apis.v1.utils.users_utils import get_order_by_query


class UsersService():

    def __init__(self, db):
        self.db = db
    
    def get_total_records_super_admin(self) -> int:
        subquery = self.db.query(idp_users.id) \
        .join(idp_user_apps_roles, idp_users.id == idp_user_apps_roles.idp_users_id, isouter=True) \
        .join(sp_apps_role, idp_user_apps_roles.sp_apps_role_id == sp_apps_role.id, isouter=True) \
        .join(roles, sp_apps_role.roles_id == roles.id, isouter=True) \
        .filter(and_(roles.name != "super-admin",idp_users.is_approved == True)) \
        .subquery()
        count_records = self.db.query(idp_users.id).filter(idp_users.id.in_(select(subquery))).count()
        return count_records

    def get_total_records_sub_admin(self) -> int:
        subquery = self.db.query(idp_users.id) \
        .join(idp_user_apps_roles, idp_users.id == idp_user_apps_roles.idp_users_id, isouter=True) \
        .join(sp_apps_role, idp_user_apps_roles.sp_apps_role_id == sp_apps_role.id, isouter=True) \
        .join(roles, sp_apps_role.roles_id == roles.id) \
        .filter(and_(roles.name != "super-admin",roles.name != "sub-admin",idp_users.is_approved == True)) \
        .subquery()
        count_records = self.db.query(idp_users.id).filter(idp_users.id.in_(select(subquery))).count()
        return count_records

    def get_external_users_info_db(self,user_type_id:int, page_limit:int, page_offset:int,order_by:str,latest:bool,search:str,user_status:bool,\
        
        select_practices:str) -> tuple:

        try:
            get_order_by= get_order_by_query(order_by,latest)
            count_records = self.db.query(idp_users.id).filter(and_(idp_users.user_type_id == user_type_id,idp_users.is_approved == True)).count()
            subquery = self.db.query(idp_users.id).filter(and_(idp_users.user_type_id == user_type_id,idp_users.is_approved == True))\
                .order_by(idp_users.id.asc()).limit(page_limit).offset(page_offset*page_limit).subquery()

            if search is None and select_practices =='All':
                users_info_object = self.db.query(idp_users,SPAPPS).order_by(get_order_by).filter(idp_users.id.in_(select(subquery))) \
                .join(idp_sp, idp_users.id == idp_sp.idp_users_id, isouter=True).join(SPAPPS, idp_sp.sp_apps_id == SPAPPS.id, isouter=True).all()
            elif search is None and select_practices !='All' :
                users_info_object=self.db.query(idp_users,SPAPPS).filter(SPAPPS.name.ilike(f"%{select_practices}%")).filter(idp_users.id.in_(select(subquery))) \
                .join(idp_sp, idp_users.id == idp_sp.idp_users_id, isouter=True).join(SPAPPS, idp_sp.sp_apps_id == SPAPPS.id, isouter=True).all()
            elif search is not None and select_practices !='All' :
                users_info_object=self.db.query(idp_users,SPAPPS).filter(and_( SPAPPS.name.ilike(f"%{select_practices}%"),idp_users.username.ilike(f"%{search}%"))).filter(idp_users.id.in_(select(subquery))) \
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

    def get_internal_external_users_info_db(self,user_role:str, page_limit:int, page_offset:int,order_by:str,latest:bool,search:str,user_status:bool,\
        select_practices:str) -> tuple:
        try:
            get_order_by= get_order_by_query(order_by,latest)
            if user_role == "super-admin":
                
                if (user_status == True):
                    subquery = self.db.query(idp_users.id).distinct().order_by(get_order_by) \
                    .join(idp_user_apps_roles, idp_users.id == idp_user_apps_roles.idp_users_id, isouter=True) \
                    .join(sp_apps_role, idp_user_apps_roles.sp_apps_role_id == sp_apps_role.id, isouter=True) \
                    .join(roles, sp_apps_role.roles_id == roles.id, isouter=True) \
                    .filter(and_(roles.name != "super-admin",idp_users.is_approved == True,idp_users.is_active == True)).limit(page_limit).offset(page_offset*page_limit).subquery()
                elif (user_status==False):
                    subquery = self.db.query(idp_users.id).distinct().order_by(get_order_by) \
                    .join(idp_user_apps_roles, idp_users.id == idp_user_apps_roles.idp_users_id, isouter=True) \
                    .join(sp_apps_role, idp_user_apps_roles.sp_apps_role_id == sp_apps_role.id, isouter=True) \
                    .join(roles, sp_apps_role.roles_id == roles.id, isouter=True) \
                    .filter(and_(roles.name != "super-admin",idp_users.is_approved == True,idp_users.is_active == False)).limit(page_limit).offset(page_offset*page_limit).subquery()
                else:
                    subquery = self.db.query(idp_users.id).distinct().order_by(get_order_by) \
                    .join(idp_user_apps_roles, idp_users.id == idp_user_apps_roles.idp_users_id, isouter=True) \
                    .join(sp_apps_role, idp_user_apps_roles.sp_apps_role_id == sp_apps_role.id, isouter=True) \
                    .join(roles, sp_apps_role.roles_id == roles.id, isouter=True) \
                    .filter(and_(roles.name != "super-admin",idp_users.is_approved == True)).limit(page_limit).offset(page_offset*page_limit).subquery()
 
                count_records = self.get_total_records_super_admin()
                
                subquery = self.db.query(idp_users.id) \
                .order_by(idp_users.id.asc()).filter(idp_users.id.in_(select(subquery))).subquery()
                
            elif user_role == "sub-admin":
                if (user_status == True):
                    subquery = self.db.query(idp_users.id).distinct().order_by(get_order_by) \
                    .join(idp_user_apps_roles, idp_users.id == idp_user_apps_roles.idp_users_id, isouter=True) \
                    .join(sp_apps_role, idp_user_apps_roles.sp_apps_role_id == sp_apps_role.id, isouter=True) \
                    .join(roles, sp_apps_role.roles_id == roles.id) \
                    .filter(and_(roles.name != "super-admin",roles.name != "sub-admin",idp_users.is_approved == True,idp_users.is_active == True)).limit(page_limit).offset(page_offset*page_limit) \
                    .subquery()
                elif (user_status==False):
                    subquery = self.db.query(idp_users.id).distinct().order_by(get_order_by) \
                    .join(idp_user_apps_roles, idp_users.id == idp_user_apps_roles.idp_users_id, isouter=True) \
                    .join(sp_apps_role, idp_user_apps_roles.sp_apps_role_id == sp_apps_role.id, isouter=True) \
                    .join(roles, sp_apps_role.roles_id == roles.id) \
                    .filter(and_(roles.name != "super-admin",roles.name != "sub-admin",idp_users.is_approved == True,idp_users.is_active == False)).limit(page_limit).offset(page_offset*page_limit) \
                    .subquery()
                else:
                    subquery = self.db.query(idp_users.id).distinct().order_by(get_order_by) \
                    .join(idp_user_apps_roles, idp_users.id == idp_user_apps_roles.idp_users_id, isouter=True) \
                    .join(sp_apps_role, idp_user_apps_roles.sp_apps_role_id == sp_apps_role.id, isouter=True) \
                    .join(roles, sp_apps_role.roles_id == roles.id) \
                    .filter(and_(roles.name != "super-admin",roles.name != "sub-admin",idp_users.is_approved == True)).limit(page_limit).offset(page_offset*page_limit) \
                    .subquery()

                count_records = self.get_total_records_sub_admin()

                subquery = self.db.query(idp_users.id) \
                .order_by(idp_users.id.asc()).filter(idp_users.id.in_(select(subquery))).subquery()
            

            if search is None and select_practices =='All':
                users_info_object = self.db.query(idp_users,SPAPPS).order_by(get_order_by).filter(idp_users.id.in_(select(subquery))) \
                .join(idp_sp, idp_users.id == idp_sp.idp_users_id, isouter=True).join(SPAPPS, idp_sp.sp_apps_id == SPAPPS.id, isouter=True).all()
            elif search is None and select_practices !='All' :
                users_info_object=self.db.query(idp_users,SPAPPS).order_by(get_order_by).filter(SPAPPS.name.ilike(f"%{select_practices}%")).filter(idp_users.id.in_(select(subquery))) \
                .join(idp_sp, idp_users.id == idp_sp.idp_users_id, isouter=True).join(SPAPPS, idp_sp.sp_apps_id == SPAPPS.id, isouter=True).all()
            elif search is not None and select_practices !='All' :
                users_info_object=self.db.query(idp_users,SPAPPS).order_by(get_order_by).filter(and_( SPAPPS.name.ilike(f"%{select_practices}%"),idp_users.username.ilike(f"%{search}%"))).filter(idp_users.id.in_(select(subquery))) \
                .join(idp_sp, idp_users.id == idp_sp.idp_users_id, isouter=True).join(SPAPPS, idp_sp.sp_apps_id == SPAPPS.id, isouter=True).all()
            elif search is not None and select_practices =='All' :
                users_info_object=self.db.query(idp_users,SPAPPS).order_by(get_order_by).filter(idp_users.username.ilike(f"%{search}%")).filter(idp_users.id.in_(select(subquery))) \
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
