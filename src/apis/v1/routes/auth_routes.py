from os import access
from fastapi import Depends, HTTPException, Request, APIRouter, Response
from src.apis.v1.core.project_settings import Settings
from src.apis.v1.controllers.auth_controller import AuthController
from src.apis.v1.db.session import engine, get_db
from sqlalchemy.orm import Session
from src.apis.v1.validators.auth_validators import EmailValidator, EmailValidatorError, EmailValidatorOut, LoginValidator, LogoutValidator
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi_jwt_auth import AuthJWT
from redis import Redis


router = APIRouter(tags=["Authentication"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/token")

# Setup our redis connection for storing the denylist tokens
redis_conn = Redis(host='localhost', port=6379, db=0, decode_responses=True)

@AuthJWT.load_config
def get_config():
    return Settings()

@router.post("/email-verifier", summary="Email Verifier API",response_model=EmailValidatorOut,responses={422: {"model": EmailValidatorError}})
async def email_verifier(email_validator:EmailValidator,request: Request,db: Session = Depends(get_db)):
    # validate cookie
    # if unique cookie is valid, use all emails
        # if email is not valid, return error + logger("")
        # if email is valid( means found in db), return success + logger(this email {} exsist in db with success with user coming from sp)
    # if unique cookie is not valid, use only admin emails
        # if admin email is valid, return sucess message
            # cookie_idp is used when the user comes from the another sp then the user is logged in from cookie_idp
            # token is used for the authentication of apis in idp
        # if admin email is not valid return notsuccessfull
    req = await request.json()
    email = req["email"]
    resp = AuthController(db).email_verification(email)
    return resp

@router.post("/login", summary="Submit Login Page API submission")
async def sso_login(login_validator:LoginValidator,request: Request,db: Session = Depends(get_db), authorize: AuthJWT = Depends() ):
    #validate the cookie in db
    # if unique cookie is valid, use all emails
        # if email is admin: return cookie_idp + token  
        # if email is not admin and is valid sp email, return get samlrequest from uniquecookie to generate redirect response to sp
        # else: return "error"
    # if unique cookie is not valid, use only admin emails
        # if admin email is valid, return cookie_idp + token
        # if admin email is not valid return error  
    
    req = await request.json()
    email,password = req["email"],req["password"]
    resp = AuthController(db).login(email,password,authorize)
    return resp


@router.post("/refresh-token", summary="Gives new access token on every refresh token")
async def refresh_token(db: Session = Depends(get_db),authorize: AuthJWT = Depends()):
    resp = AuthController(db).create_refresh_token(authorize)
    return resp

# Create our function to check if a token has been revoked. In this simple
# case, we will just store the tokens jti (unique identifier) in redis.
# This function will return the revoked status of a token. If a token exists
# in redis and value is true, token has been revoked
@AuthJWT.token_in_denylist_loader
def check_if_token_in_denylist(decrypted_token):
    jti = decrypted_token['jti']
    print(jti)
    entry = redis_conn.get(jti)
    return (entry and entry == 'true') 

@router.post("/logout", summary="Submit Logout Page API submission")
async def sso_logout(logout_validator:LogoutValidator,request: Request, authorize: AuthJWT = Depends()):
    #validate the cookie in db
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
        
        access_token,refresh_token = req["access_token"],req["refresh_token"]
        if not access_token or not refresh_token:
            return {"message":"access token or refresh token is missing"}
        if (redis_conn.get(authorize.get_jti(access_token)) or redis_conn.get(authorize.get_jti(refresh_token))):
            return {"message":"already logged out"}




        jti = authorize.get_jti(access_token)
        redis_conn.setex(jti,Settings().access_expires,'true')
        jti = authorize.get_jti(refresh_token)
        redis_conn.setex(jti,Settings().refresh_expires,'true')

    except Exception as e:
        return {"message":"token has expired"}
    # resp = AuthController(db).logout(authorize)
    # return resp
    return {
        "message":"succesfully logged out"
    }

@router.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(),db: Session = Depends(get_db), authorize: AuthJWT = Depends()):

    resp = AuthController(db).login(form_data.username, form_data.password, authorize)
    return resp

@router.post('/fresh-login')
async def fresh_login(request: Request,login_validator:LoginValidator,db: Session = Depends(get_db), authorize: AuthJWT = Depends()):
    """
    Fresh login endpoint. This is designed to be used if we need to
    make a fresh token for a user (by verifying they have the
    correct username and password). Unlike the standard login endpoint,
    this will only return a new access token, so that we don't keep
    generating new refresh tokens, which entirely defeats their point.
    """
    req = await request.json()
    email,password = req["email"],req["password"]
    resp = AuthController(db).fresh_login(email,password,authorize)
    return resp

# A token in denylist will not be able to access this any more
@router.get('/test-token')
def protected(authorize: AuthJWT = Depends()):
    authorize.jwt_required()

    current_user = authorize.get_jwt_subject()
    return {"user": current_user}