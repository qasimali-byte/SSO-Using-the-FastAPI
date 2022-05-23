from datetime import datetime
from src.apis.v1.models.user_idp_sp_apps_model import user_idp_sp_app
from src.apis.v1.models.idp_users_model import idp_users
from src.apis.v1.models.sp_apps_model import SPAPPS


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
            # 1.
# children = session.query(Child).filter(Child.parents.any(Parent.id==??))
# 2.
# children = session.query(Child).join(Parent, Child.parents).filter(Parent.id == 99)
# 3.
# my_parent = session.query(Parent).get(2)
# children = session.query(Child).with_parent(my_parent).all()
            value = self.db.query(idp_users).filter_by(email=user_email).first()
            # print(vars(value[1]))
            v = self.db.query(idp_users).join(user_idp_sp_app, idp_users.id == value.id).all()
            for i in v:
                print(vars(i.sp_apps_relation[0]),vars(i))
            # print(vars(v[0]))
            print(v)
            # v=self.db.query(idp_users).join(user_idp_sp_app_table, idp_users.id == user_idp_sp_app_table.sp_apps_id).all()
            # v = self.db.query(SPAPPS).filter(SPAPPS.parents.any(idp_users.id==value[1].id))
            # print(vars(v))
            # print(vars(v[0]))
        except Exception as e:
            print("Error: {}".format(e))

    # def get_sps_by_id(self, sps_id):
    #     return self.db.get_sps_by_id(sps_id)

    # def get_sps_by_name(self, sps_name):
    #     return self.db.get_sps_by_name(sps_name)

    # def get_sps_by_ip(self, sps_ip):
    #     return self.db.get_sps_by_ip(sps_ip)

    # def get_sps_by_mac(self, sps_mac):
    #     return self.db.get_sps_by_mac(sps_mac)

    # def get_sps_by_type(self, sps_type):
    #     return self.db.get_sps_by_type(sps_type)

    # def get_sps_by_status(self, sps_status):
    #     return self.db.get_sps_by_status(sps_status)

    # def get_sps_by_location(self, sps_location):
    #     return self.db.get_sps_by_location(sps_location)

    # def get_sps_by_owner(self, sps_owner):
    #     return self.db.get_sps_by_owner(sps_owner)

    # def get_sps_by_description(self, sps_description):
    #     return self.db.get_sps_by_description(sps_description)

    # def get_sps_by_created_by(self, sps_created_by):
    #     return self.db.get_sps_by_created_by(sps_created_by)

    # def get_sps_by_created_date(self, sps_created_date):
    #     return self.db.get_sps_by_created_date(sps_created_date)

    # def get_sps_by_updated_by(self, sps_updated_by):
    #     return