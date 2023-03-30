from datetime import datetime, timedelta
import math
from typing import List
from sqlalchemy import and_, distinct, func, or_
from src.apis.v1.helpers.custom_exceptions import CustomException
from src.apis.v1.models.idp_user_apps_roles_model import idp_user_apps_roles
from src.apis.v1.models.idp_users_model import idp_users
from src.apis.v1.models.roles_model import roles
from src.apis.v1.models.sp_apps_model import SPAPPS
from fastapi import status, HTTPException
from src.apis.v1.models.sp_apps_role_model import sp_apps_role
from src.apis.v1.models.user_idp_sp_apps_model import idp_sp
from src.apis.v1.models.two_factor_authentication_model import two_factor_authentication
from sqlalchemy import desc
from dateutil.parser import parse
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
        print('DB Cookie--',res.cookie_id,'Request Cookie--',phone_cookie)
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



    def get_users_sp_apps_account_access_requests(self, page: int = 1, limit: int = 10, search: str = None, order_by: str = 'requested_date', latest: bool = True,status_filter: List[str] = None,
                                                  from_date: str = None, to_date: str = None):
        query = (
            self.db.query(
                idp_users.id.label('id'), 
                idp_users.username.label('username'), 
                idp_users.email.label('email'), 
                idp_sp.requested_email.label('requested_email'), 
                idp_sp.requested_user_id.label('requested_user_id'), 
                idp_sp.requested_date.label('requested_date'), 
                SPAPPS.display_name.label('sp_app_name'), 
                SPAPPS.id.label('sp_app_id'),
                SPAPPS.logo_url.label('sp_apps_logo'),
                idp_sp.is_accessible.label('is_accessible'),
                idp_sp.action.label('action').label('action')
            )
            .select_from(idp_users)
            .join(idp_sp, idp_users.id == idp_sp.idp_users_id)
            .join(SPAPPS, idp_sp.sp_apps_id == SPAPPS.id)
            .filter(idp_sp.is_requested == True, idp_sp.is_verified == True, idp_sp.action.is_not(None))
        )

        if search:
            query = query.filter(
                or_(
                    idp_users.username.ilike(f"%{search}%"),
                    idp_users.email.ilike(f"%{search}%"),
                    SPAPPS.name.ilike(f"%{search}%"),
                    idp_sp.requested_email.ilike(f"%{search}%"),
                )
            )

        if status_filter==['All']:
            query = query.filter(idp_sp.action.in_(["pending", "approved", "rejected"])) # Add default statuses
        elif status_filter!=['All']:
            query = query.filter(idp_sp.action.in_(status_filter))

        if from_date and to_date:
            from_datetime = from_date
            to_datetime = to_date + timedelta(days=1)
            query = query.filter(idp_sp.requested_date >= from_datetime, idp_sp.requested_date < to_datetime)



        total_results = (
            self.db.query(func.count(distinct(idp_users.id)))
            .join(idp_sp, idp_users.id == idp_sp.idp_users_id)
            .filter(idp_sp.is_requested == True, idp_sp.is_verified == True, idp_sp.is_accessible == False)
            .scalar()
        )

        results = (
            query
            .group_by(idp_users.id, idp_sp.requested_email, idp_sp.requested_user_id, idp_sp.requested_date, SPAPPS.name, SPAPPS.id, idp_sp.is_accessible,idp_sp.action)
            .order_by(idp_users.id, desc(order_by) if latest else order_by)
            .all()
        )

        users_dict = {}
        for result in results:
            if result.id in users_dict:
                users_dict[result.id]['sp_apps'].append({
                    'requested_email': result.requested_email,
                    'requested_user_id': result.requested_user_id,
                    'sp_app_name': result.sp_app_name,
                    'sp_app_id': result.sp_app_id,
                    'sp_apps_logo': result.sp_apps_logo,
                    'is_accessible': result.is_accessible,
                    'status':result.action
                    })
                current_user_requested_date = parse(users_dict[result.id]['requested_date'])
                if result.requested_date > current_user_requested_date:
                    users_dict[result.id]['requested_date'] = result.requested_date.isoformat()
            else:
                users_dict[result.id] = {
                    'id': result.id,
                    'username': result.username,
                    'email': result.email,
                    'requested_date': result.requested_date.isoformat(),
                    'sp_apps': [{
                        'requested_email': result.requested_email,
                        'requested_user_id': result.requested_user_id,
                        'sp_app_name': result.sp_app_name,
                        'sp_app_id': result.sp_app_id,
                        'sp_apps_logo': result.sp_apps_logo,
                        'is_accessible': result.is_accessible,
                        'status':result.action,
                    }]
                }

        users_list = []
        # Paginate by user ID, not by the sp_apps ID
        users_list = []
        user_ids = sorted(users_dict.keys())
        user_ids = user_ids[(page - 1) * limit : page * limit]
        for user_id in user_ids:
            users_list.append(users_dict[user_id])
        
        # Split users_list into pages
        total_results = len(users_list)
    
        return {
            'total_results': total_results,
            'page': page,
            'limit': limit,
            'users_list': users_list,
            'message':'successfully fetched account access request data',
            'statuscode':200
            
        }
