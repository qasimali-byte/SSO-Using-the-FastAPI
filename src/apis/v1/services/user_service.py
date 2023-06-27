from datetime import datetime
import json
from src.apis.v1.controllers.sps_controller import SPSController
from src.apis.v1.models.idp_user_apps_roles_model import idp_user_apps_roles
from src.apis.v1.models.practice_regions_model import practice_regions
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
from fastapi import HTTPException, status
from ..utils.auth_utils import create_password_hash
from ..validators.common_validators import SuccessfulJsonResponseValidator
from sqlalchemy.orm import aliased, load_only,Load
from src.apis.v1.models.idp_users_sp_apps_email_model import idp_users_sp_apps_email
import asyncio
import aiohttp
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
                file_remover(f"./public/profile_image/{existing_image_file_name}")

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
            raise CustomException(str(e) + "error occurred in user service", status.HTTP_500_INTERNAL_SERVER_ERROR)

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
            
            if values[1].id == 3:
                data = self.db.query(practices).options(Load(practices).load_only("id", "name", "dr_iq_practice_id")) \
                    .join(practice_regions, practices.region_id == practice_regions.id) \
                    .filter(practices.sp_apps_id == values[1].id) \
                    .with_entities(practices.id, practices.name, practice_regions.name, practice_regions.id, practices.dr_iq_practice_id) \
                    .all()

                for practices_values in data:
                    region_id = str(practices_values[3])  # Region ID
                    practice_id = practices_values[0]  # Practice ID
                    practice_name = practices_values[1]  # Practice Name
                    dr_iq_practice_id = practices_values[4]  # dr_iq_practice_id
                    # Create a new region dictionary if it doesn't exist in regions_list
                    if region_id not in regions_list:
                        regions_list[region_id] = {
                            "id": region_id,
                            "name": practices_values[2],  # Region Name
                            "practices": []
                        }

                    # Append the practice details to the corresponding region
                    regions_list[region_id]['practices'].append({
                        "id": practice_id,
                        "name": practice_name,
                        "dr_iq_practice_id": dr_iq_practice_id
                    })

                regions_list = list(regions_list.values())
            else:
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

    
    def submit_account_access_requests(self, idp_users_id, submit_account_access_validator):
        sp_apps_ids=submit_account_access_validator.sp_apps_ids
        is_user_already_requested=self.db.query(idp_sp).\
                filter(idp_sp.idp_users_id == idp_users_id,
                    idp_sp.sp_apps_id.in_(sp_apps_ids),
                    idp_sp.is_verified == True,
                    idp_sp.is_accessible != True,
                    idp_sp.is_requested==True,
                    ).all()     
        if is_user_already_requested:
            return {'message':'already submitted account access request','statuscode':409}

        else:
            if self.db.query(idp_sp).\
                        filter(idp_sp.idp_users_id == idp_users_id ,
                            idp_sp.sp_apps_id.in_(sp_apps_ids),
                            idp_sp.is_verified == True ,
                            idp_sp.is_accessible != True).\
                        update({idp_sp.is_requested: True,idp_sp.action:'pending', idp_sp.requested_date: datetime.utcnow()}):
                self.db.commit()

              
                return {'message': 'account access request successfully sent to super admin', 'statuscode':200}
            else:
                raise HTTPException(status_code=404, detail="Request not found")

        
    
    
    


    def delete_sp_apps_account_access_email(self, idp_users_id, user_primary_email, sp_apps_ids):
        result = {"statuscode": None, "message": None}
        print(idp_users_id, user_primary_email, sp_apps_ids)
        try:
            rows_deleted = self.db.query(idp_users_sp_apps_email).filter(
                idp_users_sp_apps_email.idp_users_id == idp_users_id,
                idp_users_sp_apps_email.primary_email == user_primary_email,
                idp_users_sp_apps_email.sp_apps_id.in_(sp_apps_ids)
            ).delete(synchronize_session=False)

            if rows_deleted > 0:
                result["statuscode"] = 200
                result["message"] = "Account access requests have been updated successfully."
                self.db.commit()
            else:
                result["statuscode"] = 404
                result["message"] = "No matching record found to delete."
                self.db.rollback()
        except Exception as e:
            self.db.rollback()
            result["statuscode"] = 500
            result["message"] = f"An error occurred while deleting the records: {str(e)}"
        finally:
            self.db.close()

        return result

    
    def add_sp_apps_account_access_email(self,idp_users_id,user_primary_email,sp_apps_ids):
        
        existing_idp_sp = self.db.query(idp_users_sp_apps_email).filter(idp_users_sp_apps_email.idp_users_id==idp_users_id,\
        idp_users_sp_apps_email.sp_apps_id.in_(sp_apps_ids)).first()
        if existing_idp_sp:
            return {'message':"User Already Approved",'statuscode':409}
        else:
            try:
                users_data=self.db.query(idp_sp).filter(idp_sp.idp_users_id == idp_users_id, idp_sp.sp_apps_id.in_([sp_apps_ids] if isinstance(sp_apps_ids, int) else sp_apps_ids),\
                    idp_sp.is_verified == True,
                    idp_sp.is_requested==True,
                    idp_sp.is_accessible==True).all()
                if users_data:
                    data_to_insert = []
                    for user in users_data:
                        sp_apps_ids = [user.sp_apps_id] if isinstance(user.sp_apps_id, int) else user.sp_apps_id
                        for sp_apps_id in sp_apps_ids:
                            app = self.db.query(SPAPPS).filter_by(id=sp_apps_id).first()
                            data = {
                                'idp_users_id': user.idp_users_id,
                                'sp_apps_id': sp_apps_id,
                                'sp_apps_email': user.requested_email,
                                'primary_email': user_primary_email,
                                'sp_apps_name': app.name
                            }
                            data_to_insert.append(data)

                    self.db.execute(idp_users_sp_apps_email.__table__.insert(), data_to_insert)
                    self.db.commit()

                    return {'message': 'Account access requests updated successfully','statuscode':200}
                else:
                    return {'statuscode':404, 'message':"Request not found"}
                
            except Exception as e:
                raise CustomException(message=str(e) + self.error_string, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
    
    def get_the_requested_email_on_sp_apps(self,idp_user_id, approve_reject_account_access_validator):
        self.db.query.query(idp_sp.requested_email)\
       .filter(idp_sp.idp_users_id == idp_user_id)\
       .filter(idp_sp.sp_apps_id == approve_reject_account_access_validator.accepted_sp_apps_ids)\
       .all()

        
    
    # def approve_sso_user_on_sp_level(self,approve_reject_account_access_validator):
        
    #     user_info = UserService(self.db).get_user_info_db(approve_reject_account_access_validator.email)
        
    #     for app_id in approve_reject_account_access_validator.requested_sp_app_id:
    #         get_sp_app_data=SPSController(self.db).get_sp_app_by_id(app_id)
            
    #         approve_to_sso_user_url=get_sp_app_data[0]['approve_to_sso_user_url']
    #         requested_emails=self.get_the_requested_email_on_sp_apps(user_info.id,approve_reject_account_access_validator)
            
    #         approve_to_sso_user_payload = {"email": [email[0] for email in requested_emails]}
    #         approve_to_sso_user_response = requests.post(approve_to_sso_user_url, data=approve_to_sso_user_payload)
            
    #         approve_to_sso_user_json = approve_to_sso_user_response.json()
    #         if approve_to_sso_user_json.get("code") == 200:
    
    
    
    
    
    # def approve_reject_account_access_requests(self, approve_reject_account_access_validator):
    #     user_info = UserService(self.db).get_user_info_db(approve_reject_account_access_validator.email)
    #     accepted_sp_apps_ids = approve_reject_account_access_validator.accepted_sp_apps_ids
    #     rejected_sp_apps_ids = approve_reject_account_access_validator.rejected_sp_apps_ids
    #     try:
    #         if accepted_sp_apps_ids:
    #             self.db.query(idp_sp).\
    #                 filter(idp_sp.idp_users_id == user_info.id,
    #                     idp_sp.sp_apps_id.in_(accepted_sp_apps_ids),
    #                     idp_sp.is_verified == True,
    #                     idp_sp.is_requested == True).\
    #                 update({idp_sp.is_accessible: True, idp_sp.action: 'approved', idp_sp.action_date: datetime.utcnow()})
    #             self.db.commit()
    #             return self.add_sp_apps_account_access_email(user_info.id, user_info.email, accepted_sp_apps_ids)
            
    #         if rejected_sp_apps_ids:
    #             self.db.query(idp_sp).\
    #                 filter(idp_sp.idp_users_id == user_info.id,
    #                     idp_sp.sp_apps_id.in_(rejected_sp_apps_ids),
    #                     idp_sp.is_verified == True,
    #                     idp_sp.is_requested == True).\
    #                 update({idp_sp.is_accessible: False, idp_sp.action: 'rejected', idp_sp.action_date: datetime.utcnow()})
            
    #             self.db.commit()
    #             return self.delete_sp_apps_account_access_email(user_info.id, user_info.email, rejected_sp_apps_ids)
            
    #     except Exception as e:
    #         print(e)
    #         raise HTTPException(status_code=404, detail="Request not found")

        



    async def get_requested_emails_on_sp_apps(self, idp_user_id, sp_app_ids):
        requested_email = self.db.query(idp_sp.requested_email) \
            .filter(idp_sp.idp_users_id == idp_user_id) \
            .filter(idp_sp.sp_apps_id.in_(sp_app_ids)) \
            .filter(idp_sp.is_verified == True) \
            .filter(idp_sp.is_requested == True) \
            .one()
        return requested_email[0]

    async def send_to_sp_apps_request(self, session, url, payload):
        async with session.post(url, data=payload) as response:
            response_json = await response.json()
            return response.status, response_json


    async def approve_sso_user_on_sp_level_async(self, approve_reject_account_access_validator):
        user_info = UserService(self.db).get_user_info_db(approve_reject_account_access_validator.email)
        requested_sp_app_ids = approve_reject_account_access_validator.accepted_sp_apps_ids
        tasks = []
        async with aiohttp.ClientSession() as session:
            for app_id in requested_sp_app_ids:
                sp_app_data = SPSController(self.db).get_sp_app_by_id(app_id)
                approve_to_sso_user_url = sp_app_data[0]['approve_to_sso_user_url']
                requested_emails = await self.get_requested_emails_on_sp_apps(user_info.id, [app_id])
                print('requested_emails',requested_emails)
                approve_to_sso_user_payload = {"email": requested_emails}
                tasks.append(asyncio.create_task(self.send_to_sp_apps_request(session, approve_to_sso_user_url, approve_to_sso_user_payload)))

            responses = await asyncio.gather(*tasks)
            return [(status, response_json) for status, response_json in responses]
        
        
    async def revoke_sso_user_on_sp_level_async(self, approve_reject_account_access_validator):
        user_info = UserService(self.db).get_user_info_db(approve_reject_account_access_validator.email)
        requested_sp_app_ids = approve_reject_account_access_validator.rejected_sp_apps_ids
        tasks = []
        async with aiohttp.ClientSession() as session:
            for app_id in requested_sp_app_ids:
                sp_app_data = SPSController(self.db).get_sp_app_by_id(app_id)
                revoke_to_sso_user_url = sp_app_data[0]['deletes_to_sso_user_url']
                requested_emails = await self.get_requested_emails_on_sp_apps(user_info.id, [app_id])
                revoke_to_sso_user_payload = {"email": requested_emails}
                tasks.append(asyncio.create_task(self.send_to_sp_apps_request(session, revoke_to_sso_user_url, revoke_to_sso_user_payload)))

            responses = await asyncio.gather(*tasks)
            return [(status, response_json) for status, response_json in responses]

    
    def all_responses_successful(self, responses):
        for status, response_json in responses:
            if status != 200 or response_json.get('code') != 200:
                return False
        return True

    
    async def approve_reject_account_access_requests_async(self, approve_reject_account_access_validator):
        user_info = UserService(self.db).get_user_info_db(approve_reject_account_access_validator.email)
        accepted_sp_apps_ids = approve_reject_account_access_validator.accepted_sp_apps_ids
        rejected_sp_apps_ids = approve_reject_account_access_validator.rejected_sp_apps_ids
        try:
            if accepted_sp_apps_ids:
                responses = await self.approve_sso_user_on_sp_level_async(approve_reject_account_access_validator)
                if self.all_responses_successful(responses):
                    self.db.query(idp_sp) \
                        .filter(idp_sp.idp_users_id == user_info.id,
                                idp_sp.sp_apps_id.in_(accepted_sp_apps_ids),
                                idp_sp.is_verified == True,
                                idp_sp.is_requested == True) \
                        .update({idp_sp.is_accessible: True, idp_sp.action: 'approved', idp_sp.action_date: datetime.utcnow()})
                    self.db.commit()
                    self.add_sp_apps_account_access_email(user_info.id, user_info.email, accepted_sp_apps_ids)
                    return {"statuscode": 200, "message": "Account access requests updated successfully"}
                else:
                    raise CustomException(message=str(e) + self.error_string, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

            if rejected_sp_apps_ids:
                responses = await self.revoke_sso_user_on_sp_level_async(approve_reject_account_access_validator)
                if self.all_responses_successful(responses):
                    self.db.query(idp_sp) \
                        .filter(idp_sp.idp_users_id == user_info.id,
                                idp_sp.sp_apps_id.in_(rejected_sp_apps_ids),
                                idp_sp.is_verified == True,
                                idp_sp.is_requested == True) \
                        .update({idp_sp.is_accessible: False, idp_sp.action: 'rejected', idp_sp.action_date: datetime.utcnow()})
                    self.db.commit()
                    self.delete_sp_apps_account_access_email(user_info.id, user_info.email, rejected_sp_apps_ids)
                    return {"statuscode": 200, "message": "Account access requests updated successfully"}
                else:
                    raise CustomException(message=str(e) + self.error_string, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            print(e)
            raise HTTPException(status_code=404, detail="Request not found")
