from src.apis.v1.controllers.roles_controller import RolesController
from src.apis.v1.db.session import get_db
from sqlalchemy.orm import Session
from fastapi import Depends, status
from fastapi import HTTPException, Request
from src.apis.v1.helpers.global_helpers import remove_int_from_urls
from src.apis.v1.services.user_service import UserService
from src.packages.roles_authorizer.role_authorizer import RoleVerifier,UserEmail,UserRole

from .auth import AuthJWT

class AuthEmail:
    def __new__(cls,authorize: AuthJWT = Depends()) -> str:
        authorize.jwt_required()
        user_email = authorize.get_jwt_subject()
        return user_email

class ApiUrl:
    def __new__(cls, req: Request = None) -> tuple:
        method = req.method
        url = req.url.path
        url = remove_int_from_urls(url)

        return method,url

class AuthorizeUserRole(UserEmail,UserRole):
    def __init__(self, db, user_email, method, url) -> None:
        self.__db = db
        self.__user_email = user_email
        self.__method = method
        self.__url = url
        self.__role = None

    def __call__(self):
        user_service_object = UserService(self.__db)
        user_info = user_service_object.get_user_info_db(self.__user_email)
        role_object = RolesController(self.__db)
        self.__role= role_object.get_ezlogin_user_role(user_info.id)
        allowed_role = role_object.get_allowed_api_by_role(role_name=self.__role,method=self.__method,url=self.__url)
        if not allowed_role:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='not enough privileges to perform an action on a resource')

    def get_user_email(self):
        return self.__user_email

    def get_user_role(self):
        return self.__role

class RoleVerifierImplemented(RoleVerifier,UserEmail,UserRole):
    def __init__(self, db: Session = Depends(get_db), method_url: ApiUrl = Depends(), user_email:AuthEmail = Depends() ):

        self.db = db
        self.method_url = method_url
        self._user_email = user_email
        self.verify()

    def verify(self):
        method, url = self.method_url
        self._authorize_object = AuthorizeUserRole(self.db, self._user_email, method, url)
        self._authorize_object()
        
    def get_user_email(self):
        return self._authorize_object.get_user_email()

    def get_user_role(self):
        return self._authorize_object.get_user_role()