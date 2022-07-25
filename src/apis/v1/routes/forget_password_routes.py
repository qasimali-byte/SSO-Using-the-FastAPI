import uuid

from src.apis.v1.db.session import get_db
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, Query
from typing import Any, Optional, List
from fastapi import Depends, FastAPI, Request, Response, Cookie
from fastapi_redis_session import deleteSession, getSession, getSessionId, getSessionStorage, setSession, SessionStorage
from src.apis.v1.validators.common_validators import SuccessfulJsonResponseValidator
from src.apis.v1.controllers.user_controller import UserController
from ..utils.user_utils import get_decrypted_text, get_encrypted_text
from starlette.responses import RedirectResponse
from src.apis.v1.validators.user_validator import ForgetPasswordValidator, SetPasswordValidator
router = APIRouter(tags=["Create-Passwords"])


@router.get("/verify-email/{user_key}", summary="Verify User email through url sent in email.",
            responses={201: {"model": SuccessfulJsonResponseValidator}}, status_code=200)
async def verify_email(
        user_key: str, request: Request, response: Response, db: Session = Depends(get_db),
        session: Any = Depends(getSession),
        sessionStorage: SessionStorage = Depends(getSessionStorage)
):
    """
        This api verifies the url hit by the user through emai.
    """
    resp = UserController(db).verify_user_through_email(user_key=user_key)
    if resp.status_code==202 or resp.status_code==302:
        print("\nEmail user verified.")
        sessionData = get_encrypted_text(get_decrypted_text(user_key).split('?')[0])
        response = RedirectResponse(url="http://localhost:8088/reset-password")
        response.set_cookie(key="user_secret", value=sessionData)
        response.set_cookie(key="test", value="test value")
        setSession(response, sessionData, sessionStorage)
        # cookie_frontend.attach_to_response(response, session)
        return response


@router.post("/change-password", summary="Takes email as request body parameter.",
             responses={201: {"model": SuccessfulJsonResponseValidator}}, status_code=201)
async def change_password(email_validator:ForgetPasswordValidator, db: Session = Depends(get_db)):
    """
        This api verifies the url hit by the user through emai.
    """

    resp = UserController(db).reset_password_through_email(user_email=email_validator.email)
    return resp


@router.post("/set-password", summary="Takes password as request body parameter.",
             responses={200: {"model": SuccessfulJsonResponseValidator}}, status_code=200)
async def set_password(set_password_validator: SetPasswordValidator, request: Request,
                       session: Any = Depends(getSession),
                       sessionId: str = Depends(getSessionId),
                       sessionStorage: SessionStorage = Depends(getSessionStorage),
                       db: Session = Depends(get_db)
                       ):
    """
        This api takes password from front-end evaluating the session cookie data and saves in db.
    """
    resp = UserController(db).set_password(session=session, password=set_password_validator.password)
    deleteSession(sessionId, sessionStorage)
    return resp


@router.get("/test/{email}", summary="For Session Test.",
            responses={201: {"model": SuccessfulJsonResponseValidator}}, status_code=200)
async def test_(
        email: str, response: Response, db: Session = Depends(get_db),
        session_id: Any = Depends(getSession),
        sessionStorage: SessionStorage = Depends(getSessionStorage)
):
    """
        This api verifies the url hit by the user through emai.
    """

    session_id = uuid.uuid4()
    sessionStorage[email] = session_id
    response.set_cookie(key="response", value=session_id, httponly=True)
    return {"message":str(response),"statuscode":5000}
