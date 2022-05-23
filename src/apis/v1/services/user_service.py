from models.idp_users_model import idp_users
from models.sp_apps_model import SPAPPS


class UserService():

    def __init__(self, db):
        self.db = db

    def create_internal_idp_user(self, **kwargs):
        try:
            create_user = idp_users(
                uuid=kwargs.get('uuid'),
                organization_id=kwargs.get('organization_id'),
                username=kwargs.get('username'),
                title=kwargs.get('title'),
                first_name=kwargs.get('first_name'),
                last_name=kwargs.get('last_name'),
                email=kwargs.get('email'),
                other_email=kwargs.get('other_email'),

            )
            SPAPPS(
                idp_users_id=kwargs.get('idp_users_id'),
            )
            create_user.sp_apps_relation.append()
            self.db.add(create_user)
            self.db.commit()
            return "created idp user", 200
        except Exception as e:
            return "Error: {}".format(e), 500