import uuid
from datetime import timedelta

from fastapi_redis import redis_client
from starlette.background import BackgroundTasks

from src.apis.v1.core.project_settings import Settings
from src.apis.v1.db.session import get_db
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, Query
from typing import Any, Optional, List
from fastapi import Depends, FastAPI, Request, Response, Cookie
from src.apis.v1.validators.common_validators import SuccessfulJsonResponseValidator
from src.apis.v1.controllers.user_controller import UserController
from utils import get_redis_client
from ..utils.user_utils import get_decrypted_text, get_encrypted_text
from starlette.responses import RedirectResponse
from src.apis.v1.validators.user_validator import ForgetPasswordValidator, SetPasswordValidator

router = APIRouter(tags=["Create-Passwords"])


@router.post("/change-password", summary="Takes email as request body parameter. Reset url will be sent to this email ID",
             responses={201: {"model": SuccessfulJsonResponseValidator}}, status_code=201)
async def change_password(email_validator:ForgetPasswordValidator, db: Session = Depends(get_db)):
    """
        Allows the user to reset password.
    """
    resp = UserController(db).reset_password_through_email(user_email=email_validator.email)
    return resp


@router.get("/verify-email/{user_key}", summary="Verify User email through url sent in email.",
            responses={201: {"model": SuccessfulJsonResponseValidator}}, status_code=200)
async def verify_email(user_key: str, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    """
        This api verifies the url hit by the user through emai.
        The session id is set in cookies and that session expires after one hour or if the user has used that.
    """
    resp = UserController(db).verify_user_through_email(user_key=user_key)
    if resp.status_code==202:
        print("\nEmail user verified.")
        user_secret = get_encrypted_text(get_decrypted_text(user_key).split('?')[0])
        session_id  = uuid.uuid4().hex
        get_redis_client().setex( name=session_id, value=user_secret,
                                       time=timedelta(hours=1))
        host = Settings().SSO_FRONTEND_URL
        response = RedirectResponse(url="{}reset-password".format(host))
        # response.set_cookie(key="user_secret", value=user_secret,httponly=True)
        response.set_cookie(key="ssid", value=session_id,httponly=True)
        return response
    elif resp.status_code==302:
        return resp


@router.post("/set-password", summary="Takes password as request body parameter.",
             responses={200: {"model": SuccessfulJsonResponseValidator}}, status_code=200)
async def set_password(set_password_validator: SetPasswordValidator, request: Request,
                       db: Session = Depends(get_db)
                       ):
    """
        This api takes password from front-end evaluating the session cookie data and saves in db.
    """
    session_id = request.cookies.get("ssid","")
    resp = UserController(db).set_password(session_id=session_id, password=set_password_validator.password)

    return resp
