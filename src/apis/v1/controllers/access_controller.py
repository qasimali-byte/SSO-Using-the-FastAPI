import os
import random
import datetime

import pyotp
from starlette import status

from celery_worker import otp_sender, otp_sender_products
from src.apis.v1.controllers.async_auth_controller import AsyncAuthController
from src.apis.v1.controllers.sps_controller import SPSController
from src.apis.v1.controllers.user_controller import UserController
from src.apis.v1.helpers.custom_exceptions import CustomException
from src.apis.v1.helpers.customize_response import custom_response
from src.apis.v1.helpers.global_helpers import create_unique_id
from src.apis.v1.models import idp_users
from src.apis.v1.services.access_service import AccessService
from src.apis.v1.services.user_service import UserService
from src.apis.v1.utils.auth_utils import create_password_hash, generate_password
from src.apis.v1.utils.user_utils import get_encrypted_text, get_decrypted_text
from src.apis.v1.validators.common_validators import SuccessfulJsonResponseValidator
from src.apis.v1.validators.user_validator import CreateInternalExternalUserValidatorIn, CreateUserValidator
from test_migrate import UserMigrate
from utils import get_redis_client

redis_client = get_redis_client()


class AccessController():
    def __init__(self, db):
        self.db = db

    def send_otp_email(self, email, product_name,product_id):

        user_data = AccessService(self.db).get_user_apps_info_db(user_email=email)
        product_names = [p["product_name"] for p in user_data.get("products")]
        products_ids = [p["product_id"] for p in user_data.get("products")]
        logo = [ p["logo"] for p in user_data.get("products") if p["product_id"] == product_id][0]
        if user_data:
            if product_name in product_names or product_id in products_ids:
                OTP = ''.join([random.choice("123456789") for _ in range(6)])
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



    def verify_otp_email(self, otp_validator):
        saved_otp_hash = redis_client.get(otp_validator.email)

        if saved_otp_hash:
            saved_otp, product_id = get_decrypted_text(saved_otp_hash).split(":")
            if saved_otp == otp_validator.otp and product_id==otp_validator.app_id:
                redis_client.delete(otp_validator.email)
                data = {
                    "message": 'otp verified success',
                    "statuscode": status.HTTP_200_OK
                }
                validated_data = SuccessfulJsonResponseValidator(**data)
                return custom_response(status_code=status.HTTP_404_NOT_FOUND, data=validated_data)

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
                apps_object = UserMigrate().user_migration_request(email=validator_data.email, app_id=products_ids[0])
                user_validator = CreateInternalExternalUserValidatorIn(firstname="first name",
                                                                        lastname="last name",
                                                                        email=validator_data.email,
                                                                        type_of_user="external",
                                                                        dr_iq_gender_id=None,
                                                                        apps=[apps_object],
                                                                        is_active=True)

                UserController(self.db).create_user(user_validator.dict())
                raise CustomException(status_code=status.HTTP_200_OK, message='otp verified, user created for apps')
            else:
                raise CustomException(status_code=status.HTTP_400_BAD_REQUEST, message='Failed, wrong OTP')
        raise CustomException(status_code=status.HTTP_404_NOT_FOUND, message='Failed, OTP expired')