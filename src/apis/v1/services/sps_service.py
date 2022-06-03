from datetime import datetime
from src.apis.v1.models.user_idp_sp_apps_model import idp_sp, user_idp_sp_app
from src.apis.v1.models.idp_users_model import idp_users
from src.apis.v1.models.sp_apps_model import SPAPPS
from sqlalchemy import desc


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

    def get_sps_app(self,user_email):
        try:
            
            sp_query = self.db.query(idp_users,idp_sp,SPAPPS).join(idp_sp, idp_users.id == idp_sp.idp_users_id) \
            .join(SPAPPS, idp_sp.sp_apps_id == SPAPPS.id).filter(idp_users.email == user_email).order_by(desc(idp_sp.is_accessible == True)).all()
            serviceproviders = []
            for i in sp_query:
                x,y = (i[1],i[2])
                serviceproviders.append({"id": y.id, "name": y.name, "image":y.logo_url,"host_url":y.host, "is_accessible":x.is_accessible})

            return serviceproviders

        except Exception as e:
            return []
