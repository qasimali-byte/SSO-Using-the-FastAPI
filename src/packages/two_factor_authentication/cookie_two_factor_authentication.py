from src.apis.v1.models.two_factor_authentication_model import two_factor_authentication
from fastapi import status
from src.apis.v1.helpers.custom_exceptions import CustomException
from utils import get_redis_client
from uuid import uuid4
redis_client = get_redis_client()


def create_phone_cookie(response, user_id, db):
    # Create phone/email cookie for two-factor authentication
    # redis_client.setex(name=cookie_key, value=cookie_key)  # persistency in redis is not reliable/affordable

    session_id = store_phone_session_db(user_id, db)  # check in db and create if not already present
    response.set_cookie(key="phone_cookie", value=session_id, samesite=None, domain="attech-ltd.com", secure=True, httponly=True)
    return response


def store_phone_session_db(user_id, db):
    res = db.query(two_factor_authentication).filter(two_factor_authentication.user_id == user_id).first()
    if not res:  # user_id does not already exist in 2FA cookie table
        try:
            session_id = uuid4()
            data = {"user_id": user_id, "cookie_id": session_id}
            data = two_factor_authentication(**data)
            db.add(data)
            db.commit()
            return session_id  # "2FA cookie created successfully", status.HTTP_201_CREATED
        except Exception as e:
            raise CustomException(str(e) + "error occurred in create cookie for 2FA ", status.HTTP_500_INTERNAL_SERVER_ERROR)
    return res.cookie_id




