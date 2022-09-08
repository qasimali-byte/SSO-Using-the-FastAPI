from src.apis.v1.models.idp_user_apps_roles_model import idp_user_apps_roles
from ..helpers.custom_exceptions import CustomException
from src.apis.v1.models.idp_users_practices_model import idp_users_practices
from src.apis.v1.models.practices_model import practices
from src.apis.v1.models.sp_apps_model import SPAPPS
from src.apis.v1.services.gender_service import GenderService
from src.apis.v1.services.roles_service import RolesService
from src.apis.v1.services.type_of_user_service import TypeOfUserService
from src.apis.v1.models.idp_user_types_model import idp_user_types
from src.apis.v1.models.idp_users_model import idp_users
from src.apis.v1.models.user_idp_sp_apps_model import idp_sp
from src.apis.v1.helpers.customize_response import file_remover, custom_response
from fastapi import status
from ..utils.auth_utils import create_password_hash
from ..validators.common_validators import SuccessfulJsonResponseValidator
from sqlalchemy.orm import aliased, load_only,Load

class UserService():

    def __init__(self, db):
        self.db = db
        self.error_string: str = "error occured in user service"

    def get_user_info_db(self, user_email):
        try:
            user_info_object = self.db.query(idp_users).filter(idp_users.email == user_email).first()
            return user_info_object

        except Exception as e:
            raise CustomException(message=str(e) + self.error_string, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get_user_info_db_by_id(self, user_id):
        try:
            user_info_object = self.db.query(idp_users).options(Load(idp_users) \
            .load_only("id","first_name","last_name","email")).filter(idp_users.id == user_id).scalar()
            return user_info_object

        except Exception as e:
            raise CustomException(message= str(e) + self.error_string, status_code= status.HTTP_500_INTERNAL_SERVER_ERROR)


    def update_user_info_db(self, user_data) -> str:
        try:
            self.db.query(idp_users).filter(idp_users.email == user_data['email']).update(user_data)
            self.db.commit()
            return "User Info Updated"

        except Exception as e:
            raise CustomException(message=str(e) + self.error_string, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def update_user_info_db_by_id(self, user_data) -> str:
        try:
            self.db.query(idp_users).filter(idp_users.id == user_data['id']).update(user_data)
            self.db.commit()
            return "User Info Updated"

        except Exception as e:
            raise CustomException(message= str(e) + self.error_string, status_code= status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update_user_image_db(self,user_email,user_image_url) -> str:
        try:
            user_info_object = self.db.query(idp_users).filter(idp_users.email == user_email).first()
            existing_image_file_name = user_info_object.profile_image.split('/')[-1]
            if existing_image_file_name != 'profile_image.jpg':
                file_remover(f"./public/assets/{existing_image_file_name}")

            self.db.query(idp_users).filter(idp_users.email == user_email).update(
                {"profile_image": user_image_url})
            self.db.commit()
            return "profile image updated"

        except Exception as e:
            raise CustomException(message=str(e) + "- error occured in user service",
                                  status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def get_user_image_db(self,user_email) -> str:
        try:
            user_info_object = self.db.query(idp_users).filter(idp_users.email == user_email).first()
            return user_info_object.profile_image

        except Exception as e:
            raise CustomException(message=str(e) + "- error occured in user service",
                                  status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def save_user_verify_db(self, user_id, verification_id) -> str:
        try:
            user_info_object = self.db.query(idp_users).filter(idp_users.id == user_id).first()
            user_info_object.is_on_hold = False
            user_info_object.verification_id = verification_id
            self.db.commit()
            return "verified"

        except Exception as e:
            raise CustomException(message=str(e) + "- error occured in user service, in save_user_verify_db", \
                                  status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def verify_user_email_db(self, user_id, verification_id) -> str:
        try:
            user_info_object = self.db.query(idp_users).filter(idp_users.id == user_id).first()

            if user_info_object.verification_id == verification_id:
                user_info_object.is_on_hold = False
                user_info_object.is_active = True
                user_info_object.is_approved = True
                user_info_object.verification_id = "verified"
                self.db.commit()
                data = {
                    "message": "User Verified Successfully",
                    "statuscode": status.HTTP_202_ACCEPTED
                }
                validated_data = SuccessfulJsonResponseValidator(**data)
                response = custom_response(status_code=status.HTTP_202_ACCEPTED, data=validated_data)
            elif user_info_object.verification_id == "verified":
                data = {
                    "message": "User is already verified, url expired",
                    "statuscode": status.HTTP_302_FOUND
                }
                validated_data = SuccessfulJsonResponseValidator(**data)
                response = custom_response(status_code=status.HTTP_302_FOUND, data=validated_data)
            else:
                data = {
                    "message": "User not found",
                    "statuscode": status.HTTP_404_NOT_FOUND
                }
                validated_data = SuccessfulJsonResponseValidator(**data)
                response = custom_response(status_code=status.HTTP_404_NOT_FOUND, data=validated_data)
            return response
        except Exception as e:
            raise CustomException(message=str(e) + "- error occured in user service",
                                  status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def set_user_password_db(self,user_id, password) -> str:
        try:
            user_info_object = self.db.query(idp_users).filter(idp_users.id == user_id).first()
            if user_info_object:
                user_info_object.password_hash = create_password_hash(password)
                self.db.commit()
                data = {
                    "message": "Password saved successfully",
                    "statuscode": status.HTTP_202_ACCEPTED
                }
                validated_data = SuccessfulJsonResponseValidator(**data)
                response = custom_response(status_code=status.HTTP_202_ACCEPTED, data=validated_data)
            else:
                data = {
                    "message": "Failed to recognize.",
                    "statuscode": status.HTTP_404_NOT_FOUND
                }
                validated_data = SuccessfulJsonResponseValidator(**data)
                response = custom_response(status_code=status.HTTP_404_NOT_FOUND, data=validated_data)
            return response
        except Exception as e:
            raise CustomException(message=str(e) + "- error occured in user service",
                                  status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def create_user_db(self, user_data):
        try:
            create_user = idp_users(**user_data)
            self.db.add(create_user)
            self.db.commit()
            return create_user
        except Exception as e:
            raise CustomException(str(e) + "error occured in user service", status.HTTP_500_INTERNAL_SERVER_ERROR)

    def create_internal_idp_user(self, **kwargs):
        try:
            # choosing the sp application that needs to be accessed
            # choosing the type of user
            # insert into idp_users_practices
            # insert into idp_user_apps_roles

            type_of_user_id = TypeOfUserService(self.db).get_type_of_user_db(kwargs.get('type_of_user'))
            if type_of_user_id is None:
                return "No User Role Found", status.HTTP_404_NOT_FOUND

            internal_user_role_id = RolesService(self.db).get_internal_roles_selected_db(
                kwargs.get('internal_user_role'))
            if internal_user_role_id is None:
                return "No Internal User Role Found", status.HTTP_404_NOT_FOUND

            type_of_user_id = type_of_user_id.id
            create_user = idp_users(
                uuid=kwargs.get('uuid'),
                organization_id=kwargs.get('organization_id'),
                nhs_number=kwargs.get('nhs_number'),
                username=kwargs.get('username'),
                first_name=kwargs.get('first_name'),
                last_name=kwargs.get('last_name'),
                email=kwargs.get('email'),
                password_hash=kwargs.get('password_hash'),
                reset_password_token=kwargs.get('reset_password_token'),
                reset_password_token_expiry=kwargs.get('reset_password_token_expiry'),
                created_date=kwargs.get('created_date'),
                updated_date=kwargs.get('updated_date'),
                last_login_date=kwargs.get('last_login_date'),
                is_active=kwargs.get('is_active'),
                user_type_id=type_of_user_id,
            )

            self.db.add(create_user)
            self.db.commit()

            objects = []
            sps_object = kwargs.get('sps_object_list')
            for sp in sps_object:
                objects.append(idp_sp(
                    is_accessible=True,
                    idp_users_id=create_user.id,
                    sp_apps_id=sp.id,

                ))

            self.db.bulk_save_objects(objects)
            self.db.commit()

            user_role_data = idp_user_role(
                idp_users_id=create_user.id,
                roles_id=internal_user_role_id.id,
            )
            self.db.add(user_role_data)
            self.db.commit()

            return "created idp user", status.HTTP_201_CREATED
        except Exception as e:
            print(e, "error")
            return "Error: {}".format(e), status.HTTP_500_INTERNAL_SERVER_ERROR

    def get_practice_roles_data_for_sps(self, type_of_user, user_sp_apps, practice_roles_data):
        user_id = type_of_user[1]
        practices_als = aliased(practices, name='practices_aliased')
        for values in user_sp_apps:
            regions_list = {}
            regions = {}
            data = self.db.query(practices, practices_als).options(Load(practices).load_only("id", "name")) \
                .options(Load(practices_als).load_only("id", "name")) \
                .join(practices_als, practices.practice_region_id == practices_als.id, full=True).filter(
                practices.sp_apps_id == values[1].id) \
                .join(idp_users_practices, practices.id == idp_users_practices.practices_id).filter(
                idp_users_practices.idp_users_id == user_id) \
                .all()

            for practices_values in data:
                if practices_values[1] is None:
                    regions['id'] = str(practices_values[0].id)
                    regions['name'] = practices_values[0].name
                    if regions['id'] not in regions_list:
                        regions['practices'] = []
                        regions_list[regions['id']] = dict(regions)
                    else:
                        regions_list[regions['id']]['practices'].append(
                            {'id': practices_values[0].id, 'name': practices_values[0].name})

                else:
                    regions['id'] = str(practices_values[1].id)
                    regions['name'] = practices_values[1].name
                    if regions['id'] not in regions_list:
                        regions['practices'] = [{'id': practices_values[0].id, 'name': practices_values[0].name}]
                        regions_list[regions['id']] = dict(regions)
                    else:
                        regions_list[regions['id']]['practices'].append(
                            {'id': practices_values[0].id, 'name': practices_values[0].name})

            regions_list = [i for i in regions_list.values()]
            if values[1].name == "ez-login" and type_of_user[0].lower() == "internal":
                user_selected_roles = RolesService(self.db).get_user_selected_role(values[1].name, user_id)

                # it should be get from db
                if user_selected_roles == "super-admin":
                    user_roles = [{"id": 1, "name": "Sub Admin", "sub_roles": []},
                                  {"id": 16, "name": "Practice Admin", "sub_roles": []}]
                elif user_selected_roles == "sub-admin":
                    user_roles = [{"id": 16, "name": "Practice Admin", "sub_roles": []}]
                else:
                    user_roles = []

                if user_selected_roles != "practice-administrator":
                    practice_roles_data.insert(0, {
                        "id": values[1].id,
                        "name": values[1].name,
                        "sp_app_name": values[1].display_name,
                        "sp_app_image": values[1].logo_url,
                        "roles": user_roles,
                        "practices": []
                    })

            elif values[1].name == "dr-iq":
                user_roles = RolesService(self.db).get_apps_practice_roles(values[1].id)
                gender_data = GenderService(self.db).get_genders_db()

                practice_roles_data.append({
                    "id": values[1].id,
                    "name": values[1].name,
                    "gender": gender_data['gender'],
                    "sp_app_name": values[1].display_name,
                    "sp_app_image": values[1].logo_url,
                    "roles": user_roles,
                    "practices": regions_list
                })
            else:
                user_roles = RolesService(self.db).get_apps_practice_roles(values[1].id)
                practice_roles_data.append({
                    "id": values[1].id,
                    "name": values[1].name,
                    "sp_app_name": values[1].display_name,
                    "sp_app_image": values[1].logo_url,
                    "roles": user_roles,
                    "practices": regions_list
                })

        return practice_roles_data

    def get_all_sps_practice_roles_db(self, email):
        try:
            ## ez login should come at first
            ## internal users should not have ez login option
            ## external users should have ez login option
            ## ez login sub-admin should have only practice-admin option
            type_of_user = self.db.query(idp_users,idp_user_types) \
                            .join(idp_user_types, idp_users.user_type_id == idp_user_types.id) \
                            .with_entities(idp_user_types.user_type, idp_users.id)\
                            .filter(idp_users.email == email).first()
            practice_roles_data = []
            user_sp_apps = self.db.query(idp_users,SPAPPS) \
            .filter(idp_users.email == email) \
            .join(idp_sp,idp_users.id == idp_sp.idp_users_id) \
            .join(SPAPPS, idp_sp.sp_apps_id == SPAPPS.id).filter(SPAPPS.is_active == True).all()

            if len(user_sp_apps) > 0:
                practice_roles_data = self.get_practice_roles_data_for_sps(type_of_user, user_sp_apps,
                                                                           practice_roles_data)
                return practice_roles_data, status.HTTP_200_OK
            else:
                return practice_roles_data, status.HTTP_200_OK

        except Exception as e:
            return "Error: {}".format(e), status.HTTP_500_INTERNAL_SERVER_ERROR

    def test_insert_practices_userid(self, email, user_id):
        objects = []
        data = self.db.query(practices).with_entities(practices.id).all()
        for sp in data:
            objects.append(idp_users_practices(
                idp_users_id=user_id,
                practices_id=sp[0],

            ))

        self.db.bulk_save_objects(objects)
        self.db.commit()

    
    def delete_users_info_db(self,users_id):
        try:
            user=self.db.query(idp_users).filter(idp_users.id==users_id).one_or_none()
            if user is not None:
                # self.db.query(idp_sp).filter(idp_sp.idp_users_id==users_id).delete() # this will return the list
                # self.db.query(idp_user_apps_roles).filter(idp_user_apps_roles.idp_users_id==users_id).delete()
                # self.db.query(idp_users_practices).filter(idp_users_practices.idp_users_id==users_id).delete()
                # self.db.query(idp_users).filter(idp_users.id==users_id).delete()
                user.is_approved = False
                self.db.commit()
                return "User deleted successfully", status.HTTP_200_OK
            else:
                return "User not found", status.HTTP_404_NOT_FOUND
            
        except Exception as e:
            raise CustomException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, message=str(e)+"- error occured in user_service.py")



    def delete_user_practices_roles_db(self, user_id) -> int:
        try:
            self.db.query(idp_sp).filter(idp_sp.idp_users_id == user_id) \
            .delete(synchronize_session=False)
            self.db.query(idp_users_practices).filter(idp_users_practices.idp_users_id == user_id) \
            .delete(synchronize_session=False)
            self.db.query(idp_user_apps_roles).filter(idp_user_apps_roles.idp_users_id == user_id) \
            .delete(synchronize_session=False)
            self.db.commit()
            return 200
        except Exception as e:
            raise CustomException(str(e)+"error occured in user service", status.HTTP_500_INTERNAL_SERVER_ERROR)
