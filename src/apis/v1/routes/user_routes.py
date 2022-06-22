from datetime import datetime
from uuid import uuid4
from fastapi import Depends, HTTPException, Header, Request, APIRouter, Response
from src.apis.v1.controllers.user_controller import UsersController
from src.apis.v1.services.auth_service import AuthService
from src.apis.v1.core.project_settings import Settings
from src.apis.v1.controllers.auth_controller import AuthController
from src.apis.v1.db.session import engine, get_db
from sqlalchemy.orm import Session
from fastapi_jwt_auth import AuthJWT
from . import oauth2_scheme

from src.apis.v1.validators.user_validator import AdminUserValidator, ExternalUserValidator, InternalUserValidator, UpdateUserValidatorIn, UserInfoValidator, UserSPPracticeRoleValidatorOut, UserValidatorIn, UserValidatorOut
from src.apis.v1.utils.auth_utils import create_password_hash
from src.apis.v1.validators.common_validators import ErrorResponseValidator



router = APIRouter(tags=["User-Management"])


@router.post("/user/admin", summary="Create Admin User Api")
async def create_user(user_validator:AdminUserValidator,request: Request,db: Session = Depends(get_db)):
    """
        Create Admin User 
    """
    pass

@router.post("/user/internal", summary="Create Internal User Api", responses={201:{"model":UserValidatorOut},
            404:{"model":ErrorResponseValidator,"description":"Error Occured when not found"},
            500:{"description":"Internal Server Error","model":ErrorResponseValidator}})
async def create_internal_user(user_validator:InternalUserValidator,db: Session = Depends(get_db),authorize: AuthJWT = Depends(), token: str = Depends(oauth2_scheme)):
    """
        Create Internal User 
    """
    # data = {
    #     "firstname": "string",
    #     "lastname": "string",
    #     "email": "user@example.com",
    #     "dr_iq_gender_id":1,
    #     "type_of_user": "internal",
        # "apps": [
        #     {
        #     "id": 7,
        #     "practices": [],
        #     "role": {
        #             "id": 1,
        #             "sub_role": None
        #         }
                
        #     },
        #     {
        #     "id": 3,
        #     "practices": [
        #             {
        #             "id": 337,
        #             },
        #             {
        #             "id": 338,
        #             },
        #             {
        #             "id": 366,
        #             },
        #             {
        #             "id": 374,
        #             },
        #             {
        #             "id": 375,
        #             },
        #             {
        #             "id": 376,
        #             }
        #         ],
        #     "role": 
        #             {
        #             "id": 4,
        #             "sub_role": 3
        #             }
                
        #     }
        # ]
    # }
    # resp = UsersController(db).create_internal_user(data)
    # print(user_validator)
    resp = UsersController(db).create_internal_user(user_validator.dict())
    return resp

@router.post("/user/external", summary="Create External User Api", responses={201:{"model":UserValidatorOut}})
async def create_external_user(user_validator:ExternalUserValidator,request: Request,db: Session = Depends(get_db)):
    """
        Create External User 
    """
    req = await request.json()
    pass

@router.get("/user/service-providers/practices/roles", summary="Get All Service Providers With Practices And RolesApi",
            responses={200:{"model":UserSPPracticeRoleValidatorOut,"description":"Succesfully returned service providers with their practices and roles"},})
async def get_practice_roles(authorize: AuthJWT = Depends(), token: str = Depends(oauth2_scheme),db: Session = Depends(get_db)):
# async def get_practice_roles(db: Session = Depends(get_db)):
    """
        Get All Service Providers Practice Roles
    """
    authorize.jwt_required()
    current_user_email = authorize.get_jwt_subject()
    # current_user_email = "umair@gmail.com"
    resp = UsersController(db).get_sps_practice_roles(current_user_email)
    return resp


@router.post("/user", summary="Create User Api", responses={201:{"model":UserValidatorOut},
            404:{"model":ErrorResponseValidator,"description":"Error Occured when not found"},
            500:{"description":"Internal Server Error","model":ErrorResponseValidator}})
async def create_internal_user(user_validator:UserValidatorIn, authorize: AuthJWT = Depends(), token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """
        Create User 
    """
    authorize.jwt_required()
    current_user_email = authorize.get_jwt_subject()
    resp = UsersController(db).create_user(user_validator)
    return resp


@router.get("/user", summary="Get User Information", responses={200:{"model":UserInfoValidator}})
async def get_user_info(authorize: AuthJWT = Depends(),token: str = Depends(oauth2_scheme),db: Session = Depends(get_db)):
    """
        This api get the user information for profile
    """
    authorize.jwt_required()
    current_user_email = authorize.get_jwt_subject()
    resp = UsersController(db).get_user_info(user_email=current_user_email)
    return resp


@router.put("/user", summary="Update User Information", responses={201:{"model":UserInfoValidator}}, status_code=201)
async def update_user_info(updateuser:UpdateUserValidatorIn, authorize: AuthJWT = Depends(), token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """
        This api updates the user information for profile
    """

    authorize.jwt_required()
    current_user_email = authorize.get_jwt_subject()
    resp = UsersController(db).update_user_info(user_email=current_user_email,user_data=updateuser.dict())
    return resp