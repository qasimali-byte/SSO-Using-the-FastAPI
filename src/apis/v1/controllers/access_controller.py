import json
import os
import random
import datetime

import pyotp
import requests
from src.apis.v1.services.roles_service import RolesService
from starlette import status
from fastapi import Request, Response
from celery_worker import otp_sender, otp_sender_products, otp_sms_sender, super_admin_email_sender
from src.apis.v1.controllers.async_auth_controller import AsyncAuthController
from src.apis.v1.controllers.sps_controller import SPSController
from src.apis.v1.controllers.user_controller import UserController
from src.apis.v1.helpers.custom_exceptions import CustomException
from src.apis.v1.helpers.customize_response import custom_response
from src.apis.v1.helpers.global_helpers import create_unique_id
from src.apis.v1.models import idp_users
from src.apis.v1.services.access_service import AccessService
from src.apis.v1.services.user_service import UserService
from src.apis.v1.controllers.sps_controller import SPSController
from src.apis.v1.utils.auth_utils import create_password_hash, generate_password
from src.apis.v1.utils.user_utils import get_encrypted_text, get_decrypted_text
from src.apis.v1.validators.access_validator import GetAccountAccessRequestUsersListValidatorOut
from src.apis.v1.validators.common_validators import SuccessfulJsonResponseValidator
from src.apis.v1.validators.sps_validator import ListServiceProviderValidatorOut, ListUnAccessibleServiceProviderValidatorOut
from src.apis.v1.validators.user_validator import CreateInternalExternalUserValidatorIn, CreateUserValidator
from src.packages.usermigrations.ezanalytics import EZAnalyticsMigrate
from src.packages.usermigrations.ezweb import EZWEBMigrate
from test_migrate import UserMigrate
from utils import get_redis_client

redis_client = get_redis_client()


class AccessController():
    def __init__(self, db):
        self.db = db

    def send_email_to_super_admin(self,user_email, contact_no):
        user_info_data = UserService(self.db).get_user_info_db(user_email)
        user_role = RolesService(self.db).get_user_selected_role("ez-login", user_info_data.id)
        if user_info_data:
                user_name = user_info_data.username
                created_by = user_info_data.created_by
                task = super_admin_email_sender.delay(user_name,created_by,contact_no, user_role)
                # 2022-05-20 04:10:29.098
                return {'status_code': status.HTTP_200_OK, 'task_id': task.id}
        else:
            data = {
                "message": 'User not found',
                "statuscode": status.HTTP_404_NOT_FOUND
            }
            validated_data = SuccessfulJsonResponseValidator(**data)
            return custom_response(status_code=status.HTTP_404_NOT_FOUND, data=validated_data)



    def send_otp_email(self, email, product_name,product_id):
        user_data = AccessService(self.db).get_user_apps_info_db(user_email=email)
        product_names = [p["product_name"] for p in user_data.get("products")]
        products_ids = [p["product_id"] for p in user_data.get("products")]
        logo = [p["logo"] for p in user_data.get("products") if p["product_id"] == product_id][0]
        if user_data:
            if product_name in product_names or product_id in products_ids:
                OTP = ''.join([random.choice("123456789") for _ in range(4)])
                otp_hash = get_encrypted_text(OTP + ":" + str(product_id))
                redis_client.setex(name=email, value=otp_hash, time=15 * 60 + 5)
                date_time = datetime.datetime.now() + datetime.timedelta(minutes=15)
                natural_datetime = date_time.strftime('%I:%M:%S %p %d %b, %Y')
                data = {
                    "name": user_data.get("user").first_name,
                    "recipient": email,
                    "app": product_name,
                    "otp": OTP,
                    "expires": natural_datetime,
                    "logo": os.environ.get("SSO_BACKEND_URL") + "api/v1/" + logo
                }

                task = otp_sender.delay(user_data=data)
                # 2022-05-20 04:10:29.098
                return {'status_code': status.HTTP_200_OK, "expires": date_time, 'task_id': task.id}
            else:
                data = {
                    "message": 'product not found for this user',
                    "statuscode": status.HTTP_404_NOT_FOUND
                }
                validated_data = SuccessfulJsonResponseValidator(**data)
                return custom_response(status_code=status.HTTP_404_NOT_FOUND, data=validated_data)

        data = {
            "message": 'user not found with this email.',
            "statuscode": status.HTTP_404_NOT_FOUND
        }
        validated_data = SuccessfulJsonResponseValidator(**data)
        return custom_response(status_code=status.HTTP_404_NOT_FOUND, data=validated_data)

    async def send_otp_products_email(self, products_validator,async_db):
        """We sand OTP for selected Apps and then create user on verification for all those apps"""

        if self.db.query(idp_users).filter(idp_users.email == products_validator.email).first() is not None:
            raise CustomException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                                  message='user already exists with this email')
        products_allowed = await AsyncAuthController(async_db).find_user_ids_in_other_products(products_validator.email)
        products_allowed_ids= [p.get("id")for p in products_allowed]
        email_products = [p for p in products_allowed if str(p.get("id")) in products_validator.selected_products]
        keep_products = ''
        if len(products_validator.selected_products)==0:
            raise CustomException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                                  message='no product is selected.')
        for p in products_validator.selected_products:
            keep_products+=p+","
            if not int(p) in products_allowed_ids:
                raise CustomException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                                      message='Requested product is not allowed')

        OTP = ''.join([random.choice("0123456789") for _ in range(4)])
        otp_apps = f"{OTP}+{keep_products}"
        redis_client.setex(name=products_validator.email + ",products", value=otp_apps, time=15 * 60 + 5)
        date_time = datetime.datetime.now() + datetime.timedelta(minutes=15)
        natural_datetime = date_time.strftime('%I:%M:%S %p %d %b, %Y')
        data = {
            "name": "There",
            "recipient": products_validator.email,
            "products": email_products,
            "otp": OTP,
            "expires": natural_datetime,
        }
        task = otp_sender_products.delay(user_data=data)
        return {'status_code': status.HTTP_200_OK, "expires": date_time, 'task_id': task.id}


    async def send_otp_for_account_access_request(self, account_access_validator):

        get_sp_app_data=SPSController(self.db).get_sp_app_by_id(account_access_validator.requested_sp_app_id)
        email_verification_url=get_sp_app_data[0]['email_validation_url']
        validation_payload = {"email": account_access_validator.requested_email}
        validation_response = requests.post(email_verification_url, data=validation_payload)
        validation_json = validation_response.json()
        if validation_json.get("code") == 200:
            OTP = ''.join([random.choice("0123456789") for _ in range(4)])
            otp_apps = f"{OTP}+{str(account_access_validator.requested_sp_app_id)}"
            redis_client.setex(name=account_access_validator.requested_email + ",products", value=otp_apps, time=15 * 60 + 5)
            date_time = datetime.datetime.now() + datetime.timedelta(minutes=15)
            natural_datetime = date_time.strftime('%I:%M:%S %p %d %b, %Y')
            data = {
                "name": "There",
                "recipient": account_access_validator.requested_email,
                "products": get_sp_app_data,
                "otp": OTP,
                "expires": natural_datetime,
            }
            task = otp_sender_products.delay(user_data=data)
            return {'status_code': status.HTTP_200_OK, "expires": date_time, 'task_id': task.id}
        else:
            data= {"message": "Invalid email address",'statuscode':status.HTTP_404_NOT_FOUND}
            validated_data = SuccessfulJsonResponseValidator(**data)
            return custom_response(status_code=status.HTTP_404_NOT_FOUND, data=validated_data)
            

    def verify_otp_email(self, otp_validator):
        saved_otp_hash = redis_client.get(otp_validator.email)

        if saved_otp_hash:
            saved_otp, product_id = get_decrypted_text(saved_otp_hash).split(":")
            print(saved_otp, product_id,'otp_validator.otp',otp_validator.otp)
            if saved_otp == otp_validator.otp and int(product_id)==otp_validator.app_id:
                redis_client.delete(otp_validator.email)
                data = {
                    "message": 'otp verified success',
                    "statuscode": status.HTTP_200_OK
                }
                validated_data = SuccessfulJsonResponseValidator(**data)
                return custom_response(status_code=status.HTTP_200_OK, data=validated_data)

            data = {
                "message": 'otp verification failed',
                "statuscode": status.HTTP_404_NOT_FOUND
            }
            validated_data = SuccessfulJsonResponseValidator(**data)
            return custom_response(status_code=status.HTTP_404_NOT_FOUND, data=validated_data)
        else:
            raise CustomException(status_code=status.HTTP_404_NOT_FOUND, message='No data found for this user')

    def verify_otp_products_email(self,validator_data):
        key = validator_data.email + ",products"
        temp_data = redis_client.get(key)
        if temp_data:
            saved_otp, products = temp_data.split('+')
            products_ids = products.split(',')[0:-1]
            for p in validator_data.selected_products:
                if not p in products_ids:
                    raise CustomException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                                          message='failed, Illegal product requested.')
            if saved_otp == validator_data.otp:
                redis_client.delete(key)
                # is user requesting allowed products.
                if AccessService(self.db).if_user_exists_db(user_email=validator_data.email):
                    raise CustomException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                                          message='email already used.')
                # user = user_data.get("user")
                # idp_user_data = CreateUserValidator(uuid=create_unique_id(),
                #                                     firstname="first name",
                #                                     lastname="last name",
                #                                     email=validator_data.email,
                #                                     username=str("username"),
                #                                     password_hash=create_password_hash(generate_password(size=12)),
                #                                     user_type_id = 2,
                #                                     is_active=False,
                #                                     )
                #  create user in db
                # user_created_data = UserService(self.db).create_user_db(idp_user_data.dict())
                # SPSController(self.db).assign_sps_to_user(user_id=user_created_data.id, sps_object_list=products_ids)
                apps_list = []
                for ids in products_ids:
                    if ids == '4':
                        apps_list.append(EZAnalyticsMigrate().user_migration_request(email=validator_data.email,app_id=int(ids)))
                    elif ids == '6':
                        apps_list.append(EZWEBMigrate().user_migration_request(email=validator_data.email,app_id=int(ids)))
                    
                user_validator = CreateInternalExternalUserValidatorIn(firstname="first name",
                                                                        lastname="last name",
                                                                        email=validator_data.email,
                                                                        type_of_user="external",
                                                                        dr_iq_gender_id=None,
                                                                        apps=apps_list,
                                                                        is_active=True)

                UserController(self.db).create_user(user_validator.dict())
                raise CustomException(status_code=status.HTTP_200_OK, message='otp verified, user created for apps and reset password mail has been generated')
            else:
                raise CustomException(status_code=status.HTTP_400_BAD_REQUEST, message='Failed, wrong OTP')
        raise CustomException(status_code=status.HTTP_404_NOT_FOUND, message='Failed, OTP expired')

    def get_contact_no_by_email(self, user_email, request):
        contact_no = AccessService(self.db).get_contact_no_by_email(user_email)
        if contact_no:
            data = {"contact_no": contact_no, "cookie_verification": False}
            try:  # now check if its cookie exists
                phone_cookie = request.cookies.get("phone_cookie")
                res = AccessService(self.db).get_two_factor_authentication_cookie(contact_no, phone_cookie)
                if res:
                    data["cookie_verification"] = True
            except Exception as err:
                print(err)
            return custom_response(data=data, status_code=status.HTTP_200_OK)
        data = {"message": "contact_no not found in db", "status_code": 404}
        return custom_response(data=data, status_code=status.HTTP_404_NOT_FOUND)

    def send_otp_sms(self, email, contact_no):
        res = AccessService(self.db).if_user_exists_db(email)
        if res:
            otp_sms = ''.join([random.choice("123456789") for _ in range(4)])
            otp_sms_hash = get_encrypted_text(otp_sms)
            redis_client.setex(name=contact_no, value=otp_sms_hash, time=15 * 60 + 5)
            date_time = datetime.datetime.now() + datetime.timedelta(minutes=15)
            data = { "contact_no": contact_no, "otp": otp_sms}
            task = otp_sms_sender.delay(user_data=data)
            # res = self.get_contact_no_by_email(email, "")
            # if res.status_code == status.HTTP_404_NOT_FOUND:
            #     AccessService(self.db).save_contact_no_db(email, contact_no)
            return {'status_code': status.HTTP_200_OK, "expires": date_time, 'task_id': task.id}
        return custom_response(data={"message": "user email not found in db", "status_code": 404}, status_code=status.HTTP_404_NOT_FOUND)

    def verify_otp_sms(self,email, otp_sms, contact_no):
        saved_otp_sms_hash = redis_client.get(contact_no)
        if saved_otp_sms_hash:
            saved_otp_sms = get_decrypted_text(saved_otp_sms_hash)
            if saved_otp_sms == otp_sms:
                redis_client.delete(contact_no)
                res = self.get_contact_no_by_email(email, "")
                # if contact_no is not already in db then saving it for future purpose
                if res.status_code == status.HTTP_404_NOT_FOUND:
                    AccessService(self.db).save_contact_no_db(email, contact_no)
                return custom_response(status_code=status.HTTP_200_OK, data={"message": 'OTP Verification Succeeded', "status_code": 200})
            return custom_response(status_code=status.HTTP_406_NOT_ACCEPTABLE, data={"message": 'OTP Verification Failed', "status_code": 406})
        else:
            return custom_response(status_code=status.HTTP_404_NOT_FOUND, data={"message": 'OTP-SMS Expired', "status_code": 404})


    def get_user_apps_info_db(self,user_email):
        
        '''
        this function will return the list of all those spapps,
        verified/not verified/not accessible
        '''
        user_info=UserService(self.db).get_user_info_db(user_email)
        user_spapps_info=SPSController(self.db).get_spapps_status(user_info.id)
        user_spapps_info = json.loads(user_spapps_info)
        user_spapps_info = ListUnAccessibleServiceProviderValidatorOut(serviceproviders=user_spapps_info)
        return user_spapps_info
    
    def add_user_verification_request(self,current__user_email,account_access_verify_validator):
        
        user_info=UserService(self.db).get_user_info_db(current__user_email)
        response=SPSController(self.db).add_verified_sp_apps(user_info.id,account_access_verify_validator)
        if response['statuscode']==409:
            return response
        else:
            return response
             
            
    def verify_account_access_otp(self,current_user_email,account_access_verify_validator):
        key = account_access_verify_validator.requested_email + ",products"
        print(current_user_email)
        temp_data = redis_client.get(key)
        if temp_data:
            print(temp_data)
            saved_otp, products = temp_data.split('+')
            if str(account_access_verify_validator.requested_sp_app_id)!= products:
                raise CustomException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                                        message='failed, Invalid product requested.')
            if saved_otp == account_access_verify_validator.otp:
                return self.add_user_verification_request(current_user_email,account_access_verify_validator)
                # raise CustomException(status_code=status.HTTP_200_OK, message='otp successfully verified')
        
            else:
                raise CustomException(status_code=status.HTTP_400_BAD_REQUEST, message='Failed, wrong OTP')
        raise CustomException(status_code=status.HTTP_404_NOT_FOUND, message='Failed, OTP expired')

    def submit_account_access_requests(self,current_user_email,submit_account_access_validator):
        user_info=UserService(self.db).get_user_info_db(current_user_email)
        response=UserService(self.db).submit_account_access_requests(user_info.id,submit_account_access_validator)
        return response
    
    def get_user_sp_apps_account_access_requests(self,page, limit, search,status_filter,from_date, to_date):
        users_data=AccessService(self.db).get_users_sp_apps_account_access_requests(page=page, limit=limit, search=search,status_filter=status_filter,from_date=from_date, to_date=to_date)
        return users_data
    
    async def approve_reject_account_access_requests(self,approve_reject_account_access_validator):
        response=await UserService(self.db).approve_reject_account_access_requests_async(approve_reject_account_access_validator)
        return response
    