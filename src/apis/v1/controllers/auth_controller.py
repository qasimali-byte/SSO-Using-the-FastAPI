from datetime import timedelta
from email import message
from sqlalchemy.orm import Session
from src.apis.v1.core.project_settings import Settings
from src.apis.v1.helpers.customize_response import custom_response
from src.apis.v1.services.auth_service import AuthService
from src.apis.v1.validators.auth_validators import EmailValidatorError, EmailValidatorOut, LoginValidator, LoginValidatorOut, RefreshTokenValidatorOut


class AuthController:

    def __init__(self, db: Session):
        self.db = db

    def login_authentication(self, email: str, password: str):
        validation = LoginValidator(email=email,password=password)
        if not validation:
            data = EmailValidatorError(
                message= "email format is not correct",
                verification=False, 
            )
            response = custom_response(data=data,status_code=422)
            return response

        user_object = AuthService(self.db).authenticate_user(email, password)
        if not user_object:
            data = EmailValidatorError(
                message= "Incorrect email or password",
                verification=False, 
            )
            response = custom_response(data=data,status_code=401)
            return response
        return user_object

    def logout(self,authorize):
        try:
            authorize.jwt_required()
        except Exception as e:
            data = {
                "message":str(e)
            }
            response = custom_response(data=data,status_code=422)
            return response
        
    def login(self, email: str, password: str, authorize):
        self.login_authentication(email, password)

        # Use create_access_token() and create_refresh_token() to create our
        # access and refresh tokens
        access_token = authorize.create_access_token(subject=email,fresh=True)
        refresh_token = authorize.create_refresh_token(subject=email)
        data = LoginValidatorOut(
            message="successfully authenticated",
            access_token= access_token, 
            refresh_token=refresh_token,
            roles= ["super_admin"], 
            token_type= "bearer")
        response = custom_response(data=data,status_code=200)
        return response
        
    def fresh_login(self, email: str, password: str, authorize):
        self.login_authentication(email, password)
            
        # Use create_access_token() and create_refresh_token() to create our
        # access and refresh tokens
        access_token = authorize.create_access_token(subject=email,fresh=True)
        data = RefreshTokenValidatorOut(
            message="successfully generated new access token",
            access_token= access_token
            )
        response = custom_response(data=data,status_code=200)
        return response

    def email_verification(self, email: str):
        if AuthService(self.db).check_email(email):
            data = EmailValidatorOut(
                message= "success",
                verification= True, 
                roles=["super_admin"], 
                email= email,
                )
            response = custom_response(data=data,status_code=200)

            
        else:
            data = EmailValidatorError(
                message= "invalid email",
                verification=False, 
            )
            response = custom_response(data=data,status_code=422)
        
        return response

    def create_refresh_token(self, authorize):
        """
        Refresh token endpoint. This will generate a new access token from
        the refresh token, but will mark that access token as non-fresh,
        as we do not actually verify a password in this endpoint.
        """
        try:
            authorize.jwt_refresh_token_required()
        except Exception as e:
            data = {
                "message":str(e)
            }
            response = custom_response(data=data,status_code=422)
            return response

        current_user = authorize.get_jwt_subject()
        new_access_token = authorize.create_access_token(subject=current_user,fresh=False)
        data = RefreshTokenValidatorOut(
            message = "successfully generated new access token",
            access_token = new_access_token
        )
        response = custom_response(data=data,status_code=200)
        return response


    