from fastapi import Depends, Form, HTTPException, Request, APIRouter, Response
from src.apis.v1.controllers.auth_controller import AuthController
from src.apis.v1.db.session import engine, get_db
from sqlalchemy.orm import Session
from src.apis.v1.validators.auth_validators import EmailValidator, EmailValidatorError, EmailValidatorOut, LoginValidator
from fastapi.security import OAuth2PasswordBearer
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

router = APIRouter(tags=["Authentication"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

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
    resp = AuthController(db).email_verifier(email)
    return resp
    # if AuthController(db).get_idp_user(email):
    #     json_compatible_item_data = jsonable_encoder({
    #         "message": "success",
    #         "verification":True, 
    #         "is_admin": True, 
    #         "email": email})
    #     response = JSONResponse(content=json_compatible_item_data)
    #     response.status_code = 200
    #     return response
    # else:
    #     json_compatible_item_data = jsonable_encoder({
    #         "message": "invalid email",
    #         "verification":False, 
    #         })
    #     response = JSONResponse(content=json_compatible_item_data)
    #     response.status_code = 422
    #     return response

@router.post("/login", summary="Submit Login Page API submission")
async def sso_login(login_validor:LoginValidator,response: Response,request: Request,db: Session = Depends(get_db), ):
    #validate the cookie in db
    # if unique cookie is valid, use all emails
        # if email is admin: return cookie_idp + token  
        # if email is not admin and is valid sp email, return get samlrequest from uniquecookie to generate redirect response to sp
        # else: return "error"
    # if unique cookie is not valid, use only admin emails
        # if admin email is valid, return cookie_idp + token
        # if admin email is not valid return error  
        # 
    req = await request.json() 
    pass

@router.post("/refresh-token", summary="Gives new access token on every refresh token")
async def refresh_token():
    pass

@router.post("/logout", summary="Submit Logout Page API submission")
async def sso_login(logout_validor:LoginValidator,response: Response,request: Request,db: Session = Depends(get_db), ):
    #validate the cookie in db
    # if unique cookie is valid, use all emails
        # if email is admin: return cookie_idp + token  
        # if email is not admin and is valid sp email, return get samlrequest from uniquecookie to generate redirect response to sp
        # else: return "error"
    # if unique cookie is not valid, use only admin emails
        # if admin email is valid, return cookie_idp + token
        # if admin email is not valid return error  
        # 
    req = await request.json() 
    pass