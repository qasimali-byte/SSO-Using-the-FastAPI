from datetime import timedelta
from email import message
from sqlalchemy.orm import Session
from src.apis.v1.core.project_settings import Settings
from src.apis.v1.helpers.customize_response import custom_response
from src.apis.v1.services.auth_service import AuthService
from src.apis.v1.services.roles_service import RolesService
from src.apis.v1.services.user_service import UserService
from src.apis.v1.validators.auth_validators import EmailValidatorError, EmailValidatorOut, LoginValidator, LoginValidatorOut, RefreshTokenValidatorOut
from fastapi import status
from src.apis.v1.services.user_service import UserService
class AuthController:

    def __init__(self, db: Session):
        self.db = db

    def login_authentication(self, email: str, password: str):
        validation = LoginValidator(email=email,password=password)
        if not validation:
            data = EmailValidatorError(
                message= "email format is not correct",
                verification=False,
                statuscode=status.HTTP_422_UNPROCESSABLE_ENTITY 
            ), 422
            return data


        user_object = AuthService(self.db).authenticate_user(email, password)
        if not user_object:
            data = EmailValidatorError(
                message= "Incorrect email or password",
                verification=False, 
                statuscode=status.HTTP_401_UNAUTHORIZED
            ), 401
            return data

        return user_object,200

    def logout(self,authorize):
        try:
            authorize.jwt_required()
        except Exception as e:
            data = {
                "message":str(e),
                "statuscode":status.HTTP_422_UNPROCESSABLE_ENTITY
            }
            response = custom_response(data=data,status_code=422)
            return response

    def login(self, email: str, password: str, authorize):
        auth_result = self.login_authentication(email, password)
        if  auth_result[1] != 200:
            response = custom_response(data=auth_result[0],status_code=auth_result[1])
            return response

        # Use create_access_token() and create_refresh_token() to create our
        # access and refresh tokens
        user_info_data = UserService(self.db).get_user_info_db(email)
        get_ezlogin_roles_only = RolesService(self.db).get_ezlogin_role_only(user_info_data.id)
        access_token = authorize.create_access_token(subject=email,roles=get_ezlogin_roles_only,fresh=True)
        refresh_token = authorize.create_refresh_token(subject=email,roles=get_ezlogin_roles_only)
        data = LoginValidatorOut(
            product_name="ezlogin",
            message="successfully authenticated",
            access_token= access_token, 
            refresh_token=refresh_token,
            roles= get_ezlogin_roles_only, 
            token_type= "bearer",
            statuscode=200)
        response = custom_response(data=data,status_code=200)
        response.set_cookie(key='refresh_token',value=refresh_token,max_age=60*60,httponly=True)
        return response
        
    def fresh_login(self, email: str, password: str, authorize):
        auth_result = self.login_authentication(email, password)
        if  auth_result[1] != 200:
            response = custom_response(data=auth_result[0],status_code=auth_result[1])
            return response
            
        # Use create_access_token() and create_refresh_token() to create our
        # access and refresh tokens
        user_info_data = UserService(self.db).get_user_info_db(email)
        get_ezlogin_roles_only = RolesService(self.db).get_ezlogin_role_only(user_info_data.id)
        access_token = authorize.create_access_token(subject=email,roles=get_ezlogin_roles_only,fresh=True)
        data = RefreshTokenValidatorOut(
            message="successfully generated new access token",
            access_token= access_token,
            statuscode=status.HTTP_200_OK
            )
        response = custom_response(data=data,status_code=200)
        return response

    def email_verification(self, email: str):
        if AuthService(self.db).check_email_initial(email):
            data = EmailValidatorOut(
                message= "success",
                verification= True, 
                roles=["super_admin"], 
                email= email,
                data=None,
                statuscode=status.HTTP_200_OK
                )
            response = custom_response(data=data,status_code=200)

            
        else:
            data = EmailValidatorError(
                message= "invalid email",
                verification=False,
                statuscode=status.HTTP_422_UNPROCESSABLE_ENTITY 
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
                "message":str(e),
                "statuscode":status.HTTP_422_UNPROCESSABLE_ENTITY
            }
            response = custom_response(data=data,status_code=422)
            return response

        current_user = authorize.get_jwt_current_user()
        user_info_data = UserService(self.db).get_user_info_db(current_user)
        get_ezlogin_roles_only = RolesService(self.db).get_ezlogin_role_only(user_info_data.id)
        new_access_token = authorize.create_access_token(subject=current_user,roles=get_ezlogin_roles_only,fresh=False)
        data = RefreshTokenValidatorOut(
            message = "successfully generated new access token",
            access_token = new_access_token,
            statuscode=status.HTTP_200_OK
        )
        response = custom_response(data=data,status_code=200)
        return response


    