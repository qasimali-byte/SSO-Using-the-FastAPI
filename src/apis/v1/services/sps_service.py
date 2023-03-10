from datetime import datetime
import json
import os
from ..helpers.custom_exceptions import CustomException
from src.apis.v1.models.user_idp_sp_apps_model import idp_sp
from src.apis.v1.models.idp_users_model import idp_users
from src.apis.v1.models.sp_apps_model import SPAPPS
from sqlalchemy import desc
from fastapi import status

class SPSService():
    def __init__(self, db):
        self.db = db

    def create_sps_model(self, **kwargs):
        try:
            spsapp = SPAPPS(
                    name = kwargs.get('name'),
                    info = kwargs.get('info'),
                    host = kwargs.get('host'),
                    sp_metadata = kwargs.get('sp_metadata'),
                    is_active = kwargs.get('is_active'),
                    created_date = datetime.now(),
                    updated_date = datetime.now(),
            )
            self.db.add(spsapp)
            self.db.commit()
            return True
        except Exception as e:
            return False

    def get_sps_app_by_name(self, name):
        try:
            value = self.db.query(SPAPPS).filter_by(name=name).first()
            print(vars(value))
            return value
        except:
            return False

    def get_all_sps(self):
        try:
            sps = self.db.query(SPAPPS).all()
            return sps
        except:
            return []

    def get_sps_app_by_filter(self, **kwargs):
        try:
            sps = self.db.query(SPAPPS).filter_by(**kwargs).all()
            return sps
        except Exception as e:
            raise CustomException(message=str(e)+"error occured in sps service", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    
    
    
    
    
    
    
    def get_sps_app(self,user_email):
        try:
            
            sp_query = self.db.query(idp_users,idp_sp,SPAPPS).join(idp_sp, idp_users.id == idp_sp.idp_users_id) \
            .join(SPAPPS, idp_sp.sp_apps_id == SPAPPS.id).filter(idp_users.email == user_email).order_by(desc(idp_sp.is_accessible == True)).all()
            serviceproviders = []
            for i in sp_query:
                x,y = (i[1],i[2])
                serviceproviders.append({"id": y.id, "display_name": y.display_name,"name": y.name, "image":y.logo_url,"host_url":y.host, "is_accessible":x.is_accessible,\
                    "sp_app_name": y.display_name,"logo_url": y.logo_url})
            return serviceproviders

        except Exception as e:
            return []
        
    def get_spapps_status(self,selected_user_id):
        try:
            
        # Generate the query and execute it to retrieve the results
            
            subquery_1 = self.db.query(idp_sp.sp_apps_id.label("app_id")).filter(
                idp_sp.idp_users_id == selected_user_id, idp_sp.is_accessible == True)
            
            subquery_2 = self.db.query(idp_sp.id, idp_sp.is_accessible, idp_sp.is_verified, 
                                            idp_sp.sp_apps_id, idp_sp.requested_email).\
                            filter(idp_sp.idp_users_id == selected_user_id, idp_sp.is_accessible == False).\
                            subquery()
            query = self.db.query(SPAPPS.id.label("app_id"), SPAPPS.name.label("app_name"),
                                        SPAPPS.display_name.label("display_name"), SPAPPS.logo_url.label("image"),
                                        subquery_2.c.is_verified.label("is_verified"), 
                                        subquery_2.c.is_accessible.label("is_accessible"),
                                        subquery_2.c.requested_email.label("requested_email")).\
                            filter(SPAPPS.id.notin_(subquery_1)).\
                            outerjoin(subquery_2, SPAPPS.id == subquery_2.c.sp_apps_id).\
                            all()

        # Convert the results to a list of dictionaries
            result_list = []
            for row in query:
                result_dict = {
                    "app_id": row["app_id"],
                    "app_name": row["app_name"],
                    "display_name": row["display_name"],
                    "image": row["image"],
                    "is_verified": row["is_verified"] or False,  # set to False if is_verified is None
                    "is_accessible": row["is_accessible"] or False,  # set to False if is_accessible is None
                    "requested_email": row["requested_email"] if row["is_verified"] else None  # set to None if is_verified is False
                }
                result_list.append(result_dict)

            # Convert the list of dictionaries to JSON
            result_json = json.dumps(result_list)
            return result_json

        except Exception as e:
            print(e)
            return []
        
    def get_sps_app_for_sp_redirections(self, user_email):
        try:
            
            sp_query = self.db.query(idp_users,idp_sp,SPAPPS).join(idp_sp, idp_users.id == idp_sp.idp_users_id) \
            .join(SPAPPS, idp_sp.sp_apps_id == SPAPPS.id).filter(idp_users.email == user_email).order_by(desc(idp_sp.is_accessible == True)).all()
            serviceproviders = []
            for i in sp_query:
                x,y = (i[1],i[2])
                serviceproviders.append({"id": y.id, "display_name": y.display_name,"name": y.name, "image":y.logo_url,"host_url":y.host, "is_accessible":x.is_accessible,\
                    "sp_app_name": y.sp_metadata,"logo_url": y.logo_url})
            return serviceproviders

        except Exception as e:
            return []

    def get_selected_unselected_sps_app(self):
        try:

            total_sp_apps = self.db.query(SPAPPS).filter(SPAPPS.is_active==True).all()
            serviceproviders = []
            for data in total_sp_apps:
                serviceproviders.append({"id": data.id, "display_name": data.display_name,"name": data.name,"host_url":data.host,\
                    "sp_app_name": data.name,"logo_url": data.logo_url})

            return serviceproviders

        except Exception as e:
            return []



    def get_selected_sps_app_for_idp_user(self,user_email):
        try:
            base_url = f"{os.environ.get('SSO_BACKEND_URL')}api/v1/"
            sp_query = self.db.query(idp_users,idp_sp,SPAPPS).join(idp_sp, idp_users.id == idp_sp.idp_users_id) \
            .join(SPAPPS, idp_sp.sp_apps_id == SPAPPS.id).filter(idp_users.email == user_email).order_by(desc(idp_sp.is_accessible == True)).all()
            serviceproviders = []
            for i in sp_query:
                y = (i[2])
                if(y.host=='dev-sso-frontend.attech-ltd.com/'):
                    serviceproviders.append(str({"name": y.name, "logo":base_url+y.logo_url,"url":'http://'+y.host}))
                else:
                    serviceproviders.append(str({"name": y.name, "logo":base_url+y.logo_url,"url":'https://'+y.host}))
                
            print(serviceproviders)
            return serviceproviders

        except Exception as e:
            return []

    def assign_sps_to_user_db(self, user_id, sps_object_list):
        try:
            objects = []
            sps_object = sps_object_list

            for sp in sps_object:
                objects.append(idp_sp(
                    is_accessible=True,
                    idp_users_id = user_id,
                    sp_apps_id  = sp,

                ))

            self.db.bulk_save_objects(objects)
            self.db.commit()
            return "assigned sps to user"

        except Exception as e:
            raise CustomException(message=str(e)+"error occured in sps service", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def add_sp_app_verification_status(self,idp_user_id,account_access_verify_validator):
        print(idp_user_id,account_access_verify_validator)
        existing_idp_sp = self.db.query(idp_sp).filter_by(idp_users_id=idp_user_id, sp_apps_id=int(account_access_verify_validator.requested_sp_app_id),\
            is_verified=True).first()
        if existing_idp_sp:
            return {'message':"App already verified",'status_code':409}
        else:
            return self.add_sp_app_verification(idp_user_id,account_access_verify_validator)
    
    def add_sp_app_verification(self,idp_user_id,account_access_verify_validator):
            new_idp_sp = idp_sp(
            idp_users_id=idp_user_id,
            sp_apps_id=int(account_access_verify_validator.requested_sp_app_id),
            is_accessible=False,
            is_verified=True,
            requested_email=account_access_verify_validator.requested_email,
            requested_user_id=account_access_verify_validator.requested_user_id,
        )
            self.db.add(new_idp_sp)
            self.db.commit()
            return {'message':"user verified successfully",'status_code':200}
        

    def get_sp_app_by_id(self, app_id):
        result = self.db.query(SPAPPS.id.label('sp_apps_id'),
                       SPAPPS.name.label('sp_apps_name'),
                       SPAPPS.logo_url.label('sp_apps_logo_url')
                       ).filter_by(is_active=True, id=app_id).one()
        app_list = [{'id': result.sp_apps_id, 'name': result.sp_apps_name, 'logo': result.sp_apps_logo_url} ]
        if len(app_list) > 0:
            return app_list
        else:
            return list([])

