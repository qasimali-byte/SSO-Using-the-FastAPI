import os
import random
import datetime

import pyotp
from starlette import status

from celery_worker import otp_sender, otp_sender_products
from src.apis.v1.helpers.custom_exceptions import CustomException
from src.apis.v1.helpers.customize_response import custom_response
from src.apis.v1.services.access_service import AccessService
from src.apis.v1.utils.user_utils import get_encrypted_text, get_decrypted_text
from src.apis.v1.validators.common_validators import SuccessfulJsonResponseValidator
from utils import get_redis_client

redis_client = get_redis_client()


class AccessController():
    def __init__(self, db):
        self.db = db

    def send_otp_email(self, email, product_name,product_id):
        # if AccessService(self.db).is_valid_email(user_email=email):
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

    def send_otp_products_email(self, email, products):
        """We sand OTP for selected Apps and then create user on verification for all those apps"""

        products = AccessService(self.db).get_user_apps_info_db(user_email=email)
        if products:
            OTP = ''.join([random.choice("0123456789") for _ in range(6)])
            redis_client.setex(name=email + ",products", value=OTP, time=15 * 60 + 5)
            date_time = datetime.datetime.now() + datetime.timedelta(minutes=15)
            natural_datetime = date_time.strftime('%I:%M:%S %p %d %b, %Y')
            data = {
                "name": products.get("user").first_name,
                "recipient": email,
                "products": products.get("products"),
                "otp": OTP,
                "expires": natural_datetime,
            }

            task = otp_sender_products.delay(user_data=data)
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

    def verify_otp_products_email(self, email, received_otp,products):
        key = email + ",products"
        saved_otp = redis_client.get(key)
        if saved_otp:
            if saved_otp == received_otp:
                redis_client.delete(key)
                #create user here
                data = {
                    "message": 'otp verified, user created for apps',
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
