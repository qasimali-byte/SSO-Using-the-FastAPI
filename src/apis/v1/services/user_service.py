from src.apis.v1.models.idp_user_types_model import idp_user_types
from src.apis.v1.models.idp_users_model import idp_users
from src.apis.v1.models.user_idp_sp_apps_model import idp_sp

class UserService():

    def __init__(self, db):
        self.db = db

    def create_internal_idp_user(self, **kwargs):
        try:

            internal_user = idp_user_types(user_type=kwargs.get('type_of_user'),created_date=kwargs.get('created_date'),
                updated_date=kwargs.get('updated_date'))
            # r = self.db.add(internal_user)
            # print(r)
            # print(vars(internal_user))
            create_user = idp_users(
                uuid=kwargs.get('uuid'),
                organization_id=kwargs.get('organization_id'),
                nhs_number=kwargs.get('nhs_number'),
                username=kwargs.get('username'),
                first_name=kwargs.get('first_name'),
                last_name=kwargs.get('last_name'),
                email=kwargs.get('email'),
                password_hash = kwargs.get('password_hash'),
                reset_password_token = kwargs.get('reset_password_token'),
                reset_password_token_expiry = kwargs.get('reset_password_token_expiry'),
                created_date=kwargs.get('created_date'),
                updated_date=kwargs.get('updated_date'),
                last_login_date=kwargs.get('last_login_date'),
                user_type_id=1,
                # user_type_id=internal_user,
            )
            # idp_sp_object = idp_sp(
            #     is_accessible = True
            # )
            # sps_object_list = kwargs.get('sps_object_list')
            # print(sps_object_list)
            # data = idp_sp_object.sp_apps_table.append(kwargs.get('sps_object_list'))
            # print(data)
            # create_user.idp_sp.append(data)
            # create_user.user_type_id.append(internal_user)
            # create_user.idp_sp.extend(kwargs.get('sps_object_list'))
            # self.db.add(create_user)
            # self.db.add(internal_user)
            # self.db.commit()
            for sp in kwargs.get('sps_object_list'):
                create_user.idp_sp.append(sp)
            idp_sp_object = idp_sp(
                is_accessible = True,
                idp_users_id = 230,
                sp_apps_id = 1
            )
            self.db.add(idp_sp_object)
            self.db.commit()
            # self.db.refresh(create_user)
            print(create_user.id)
            return "created idp user", 201
        except Exception as e:
            print(e,"error")
            return "Error: {}".format(e), 500