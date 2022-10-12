from uuid import uuid4
from fastapi import Depends, HTTPException, Request, APIRouter, Response
from fastapi import status
from fastapi_redis_session import SessionStorage, getSessionStorage
from src.apis.v1.controllers.async_auth_controller import AsyncAuthController
from src.apis.v1.helpers.global_helpers import delete_all_cookies
from src.apis.v1.helpers.html_parser import HTMLPARSER
from src.apis.v1.controllers.idp_controller import IDPController
from src.apis.v1.controllers.session_controller import SessionController
from fastapi_sessions.frontends.implementations.cookie import SessionCookie
from src.apis.v1.helpers.customize_response import custom_response
from loginprocessview import LoginProcessView
from src.apis.v1.core.project_settings import Settings
from src.apis.v1.controllers.auth_controller import AuthController
from src.apis.v1.db.session import  get_db
from sqlalchemy.orm import Session
from src.apis.v1.services.roles_service import RolesService
from src.apis.v1.services.user_service import UserService
from src.apis.v1.validators.auth_validators import EmailValidator, EmailValidatorError, EmailValidatorOut, \
    LoginValidator, LoginValidatorOut, LoginValidatorOutRedirect, LogoutValidator
from fastapi.security import OAuth2PasswordRequestForm
from src.graphql.db.session import get_session_without_context_manager
from ..helpers.auth import AuthJWT
from redis import Redis
from src.apis.v1.routes.idp_routes import cookie, cookie_frontend
from . import oauth2_scheme
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(tags=["Authentication"])
templates = Jinja2Templates(directory="templates/")

# Setup our redis connection for storing the denylist tokens
redis_conn = Redis(host=Settings().REDIS_HOST_URL, port=Settings().REDIS_HOST_PORT, db=0, decode_responses=True,password=Settings().REDIS_HOST_PASSWORD)


@AuthJWT.load_config
def get_config():
    return Settings()


@router.post("/email-verifier", summary="Email Verifier API", response_model=EmailValidatorOut,
             responses={422: {"model": EmailValidatorError},308:{"model":EmailValidatorOut}})
async def email_verifier(email_validator: EmailValidator, request: Request, db: Session = Depends(get_db), async_db: AsyncSession = Depends(get_session_without_context_manager)):
    # validate cookie
    # if unique cookie is valid, use all emails
    # if email is not valid, return error + logger("")
    # if email is valid( means found in db), return success + logger(this email {} exsist in db with success with user coming from sp)
    # if unique cookie is not valid, use only admin emails
    # if admin email is valid, return sucess message
    # cookie_idp is used when the user comes from the another sp then the user is logged in from cookie_idp
    # token is used for the authentication of apis in idp
    # if admin email is not valid return notsuccessfull
    email_dict = email_validator.dict()
    email = email_dict["email"]
    resp = AuthController(db).email_verification(email)
    if resp.status_code == 422: # user is not found in sso idp db
        resp = await AsyncAuthController(async_db).find_user_in_other_products(email)
        return resp

    return resp


@router.post("/login", summary="Submit Login Page API submission",
             responses={200: {"model": LoginValidatorOut}, 307: {"model": LoginValidatorOutRedirect}})
async def sso_login(login_validator: LoginValidator, request: Request,
                    sessionStorage: SessionStorage = Depends(getSessionStorage),
                    db: Session = Depends(get_db),
                    authorize: AuthJWT = Depends()):
    # validate the cookie in db
    # if unique cookie is valid, use all emails
    # if email is admin: return cookie_idp + token
    # if email is not admin and is valid sp email, return get samlrequest
    # from uniquecookie to generate redirect response to sp
    # else: return "error"
    # if unique cookie is not valid, use only admin emails
    # if admin email is valid, return cookie_idp + token
    # if admin email is not valid return error
    login_dict = login_validator.dict()
    email, password = login_dict["email"], login_dict["password"]
    verified_id = SessionController().verify_session(cookie_frontend, request)
    if verified_id[1] == 200:
        idp_controller = IDPController(db)
        verified_data = idp_controller.get_frontend_session_saml(verified_id[0])
        if verified_data[1] == 200:
            req = LoginProcessView()
            # validate email and password
            auth_result = AuthController(db).login_authentication(email, password)
            if auth_result[1] != 200:
                response = custom_response(data=auth_result[0], status_code=auth_result[1])
                return response
            
            status_code = req.verify_app_allowed(verified_data[0].saml_req,db,email)
            application_entity_id = req.return_sp_app_name()
            if status_code == 307:
                session = uuid4()
                req.store_session(session, email, db)
                user_info_data = UserService(db).get_user_info_db(email)
                get_ezlogin_roles_only = RolesService(db).get_ezlogin_role_only(user_info_data.id)
                access_token = authorize.create_access_token(subject=email,role=get_ezlogin_roles_only,fresh=True)
                refresh_token = authorize.create_refresh_token(subject=email,role=get_ezlogin_roles_only)
                data_out = LoginValidatorOutRedirect(access_token=access_token,refresh_token=refresh_token,message="You don't have access to this sp application",
                roles=get_ezlogin_roles_only,token_type="Bearer",redirect_url="http://dev-sso-frontend.attech-ltd.com/backend/notification",saml_response="", product_name="ez-login",
                statuscode=status.HTTP_307_TEMPORARY_REDIRECT)
                response = custom_response(data=data_out
                                        ,status_code=status.HTTP_307_TEMPORARY_REDIRECT)

                cookie.attach_to_response(response, session)
                delete_all_cookies(response, only_frontend=True)
                return response

            resp = req.get(verified_data[0].saml_req,email,db)
            resp = resp[0]
            # delete frontend cookie from redis store.
            # del sessionStorage[verified_id[0]]
            idp_controller.delete_frontend_session(verified_id[0])
            # create idp cookie
            session = uuid4()
            # store session in the redis store.
            req.store_session(session, email, db)
            # sessionStorage[session] = email
            data = HTMLPARSER().parse_html(resp["data"]["data"])
            user_info_data = UserService(db).get_user_info_db(email)
            get_ezlogin_roles_only = RolesService(db).get_ezlogin_role_only(user_info_data.id)
            access_token = authorize.create_access_token(subject=email,role=get_ezlogin_roles_only,fresh=True)
            refresh_token = authorize.create_refresh_token(subject=email,role=get_ezlogin_roles_only)
            data_out = LoginValidatorOutRedirect(access_token=access_token,refresh_token=refresh_token,message="successfully authenticated",
            roles=get_ezlogin_roles_only,token_type="Bearer",redirect_url=data[0],saml_response=data[1], product_name=application_entity_id,
            statuscode=status.HTTP_307_TEMPORARY_REDIRECT)
            response = custom_response(data=data_out
                                       , status_code=status.HTTP_307_TEMPORARY_REDIRECT)
            # response.set_cookie(key="cookie_idp", value=session, httponly=True)this and lower line are same. can be removed
            cookie.attach_to_response(response, session)
            delete_all_cookies(response, only_frontend=True)
            response.set_cookie(key='refresh_token',value=refresh_token,max_age=60*60,httponly=True)
            return response

    resp = AuthController(db).login(email, password, authorize)

    if resp.status_code == 200:
        # storing the valid cidp cookie in database
        session = uuid4()
        req = LoginProcessView()
        req.store_session(session, email, db)  # this was shifter to redis, but it was costly there.
        delete_all_cookies(resp, only_frontend=True)
        cookie.attach_to_response(resp, session)

    return resp


@router.post("/refresh-token", summary="Gives new access token on every refresh token")
async def refresh_token(db: Session = Depends(get_db), authorize: AuthJWT = Depends()):
    resp = AuthController(db).create_refresh_token(authorize)
    return resp


# Create our function to check if a token has been revoked. In this simple
# case, we will just store the tokens jti (unique identifier) in redis.
# This function will return the revoked status of a token. If a token exists
# in redis and value is true, token has been revoked
@AuthJWT.token_in_denylist_loader
def check_if_token_in_denylist(decrypted_token):
    jti = decrypted_token['jti']
    entry = redis_conn.get(jti)
    return (entry and entry == 'true')


@router.post("/logout", summary="Submit Logout Page API submission")
async def sso_logout(logout_validator: LogoutValidator, request: Request, authorize: AuthJWT = Depends()):
    # validate the cookie in db
    # if unique cookie is valid, use all emails
    # if email is admin: return cookie_idp + token
    # if email is not admin and is valid sp email, return get samlrequest from uniquecookie to generate redirect response to sp
    # else: return "error"
    # if unique cookie is not valid, use only admin emails
    # if admin email is valid, return cookie_idp + token
    # if admin email is not valid return error
    #
    try:
        req = await request.json()

        access_token, refresh_token = req["access_token"], req["refresh_token"]
        if not access_token or not refresh_token:
            response = custom_response(data={
            "message": "access token or refresh token is missing"
            }
            , status_code=status.HTTP_200_OK)
            response = delete_all_cookies(response)
            return response
            
        if (redis_conn.get(authorize.get_jti(access_token)) or redis_conn.get(authorize.get_jti(refresh_token))):
            response = custom_response(data={
            "message": "already logged out"
            }
            , status_code=status.HTTP_200_OK)
            response = delete_all_cookies(response)
            return response

        jti = authorize.get_jti(access_token)
        redis_conn.setex(jti, Settings().authjwt_access_token_expires, 'true')
        jti = authorize.get_jti(refresh_token)
        redis_conn.setex(jti, Settings().authjwt_refresh_token_expires, 'true')

    except Exception as e:
        response = custom_response(data={
        "message": "token has expired"
        }
        , status_code=status.HTTP_200_OK)
        response = delete_all_cookies(response)
        return response

    response = custom_response(data={
        "message": "successfully logged out"
    }
        , status_code=status.HTTP_200_OK)
    response = delete_all_cookies(response)
    return response


@router.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db),
                                 authorize: AuthJWT = Depends()):
    resp = AuthController(db).login(form_data.username, form_data.password, authorize)
    return resp


@router.post('/fresh-login')
async def fresh_login(request: Request, login_validator: LoginValidator, db: Session = Depends(get_db),
                      authorize: AuthJWT = Depends()):
    """
    Fresh login endpoint. This is designed to be used if we need to
    make a fresh token for a user (by verifying they have the
    correct username and password). Unlike the standard login endpoint,
    this will only return a new access token, so that we don't keep
    generating new refresh tokens, which entirely defeats their point.
    """
    req = await request.json()
    email, password = req["email"], req["password"]
    resp = AuthController(db).fresh_login(email, password, authorize)
    return resp


# A token in denylist will not be able to access this any more
@router.get('/test-token')
def protected(authorize: AuthJWT = Depends(), token: str = Depends(oauth2_scheme)):
    authorize.jwt_required()

    current_user = authorize.get_jwt_subject()
    return {"user": current_user}
