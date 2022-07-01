from datetime import datetime
from typing import List
from uuid import uuid4
from fastapi import Depends, HTTPException, Header, Request, APIRouter, Response, UploadFile, File, Form
from fastapi import Depends, HTTPException, Header, Request, APIRouter, Response
from src.apis.v1.controllers.user_controller import UsersController
from src.apis.v1.db.session import engine, get_db
from sqlalchemy.orm import Session
from ..helpers.auth import AuthJWT
from . import oauth2_scheme
from src.apis.v1.validators.user_validator import AdminUserValidator, CreateInternalExternalUserValidatorIn, CreateUserValidator, ExternalUserValidator, UpdateUserValidatorIn, UserInfoValidator, UserSPPracticeRoleValidatorOut, UserValidatorIn, UserValidatorOut
from src.apis.v1.validators.common_validators import ErrorResponseValidator, SuccessfulJsonResponseValidator

router = APIRouter(tags=["User-Management"])


@router.post("/user/admin", summary="Create Admin User Api")
async def create_user(user_validator:AdminUserValidator,request: Request,db: Session = Depends(get_db)):
    """
        Create Admin User 
    """
    pass

# @router.post("/user", summary="Create User Api", responses={201:{"model":UserValidatorOut},
#             404:{"model":ErrorResponseValidator,"description":"Error Occured when not found"},
#             500:{"description":"Internal Server Error","model":ErrorResponseValidator}})
# async def create_internal_external_user(user_validator:CreateUserValidator,db: Session = Depends(get_db),authorize: AuthJWT = Depends(), token: str = Depends(oauth2_scheme)):
#     """
#         Create User 
#     """
#     resp = UsersController(db).create_user(user_validator.dict())
#     return resp

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
    resp = UsersController(db).get_sps_practice_roles(current_user_email)
    return resp


@router.post("/user", summary="Create User Api", responses={201:{"model":UserValidatorOut},
            404:{"model":ErrorResponseValidator,"description":"Error Occured when not found"},
            500:{"description":"Internal Server Error","model":ErrorResponseValidator}})
async def create_internal_external_user(user_validator:CreateInternalExternalUserValidatorIn, authorize: AuthJWT = Depends(), token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """
        Create User 
    """
    authorize.jwt_required()
    current_user_email = authorize.get_jwt_subject()
    resp = UsersController(db).create_user(user_validator.dict())
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


@router.put("/user/profile-image", summary="Update User Profile Image", responses={201:{"model":SuccessfulJsonResponseValidator}}, status_code=200)
async def update_user_image(image:UploadFile = Form(...),authorize: AuthJWT = Depends(), token: str = Depends(oauth2_scheme),db: Session = Depends(get_db)):
    """
        This api updates the user information for profile image, uses request.body.file
    """

    authorize.jwt_required()
    current_user_email = authorize.get_jwt_subject()
    resp = UsersController(db).update_user_image(user_email=current_user_email,data_image=image)
    return resp

@router.get("/user/{user_id}/service-providers/practices/roles/", summary="Get User Information with practices and roles")
async def get_user_practices_roles_by_id(user_id:int, db: Session = Depends(get_db)):
    """
        This api get the user information for profile
    """
    resp = UsersController(db).get_user_practices_roles_by_id(user_id=user_id)
    return resp