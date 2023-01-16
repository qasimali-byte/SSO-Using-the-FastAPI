from fastapi import Depends, APIRouter, UploadFile,Form
from fastapi import Depends, HTTPException, Header, Request, APIRouter, Response
from src.apis.v1.controllers.user_controller import UserController
from src.apis.v1.db.session import engine, get_db
from sqlalchemy.orm import Session

from src.apis.v1.helpers.role_verifier import RoleVerifierImplemented
from . import oauth2_scheme
from src.apis.v1.validators.user_validator import AdminUserValidator, CreateInternalExternalUserValidatorIn, CreateUserValidator, ExternalUserValidator, GetLogedInUsersValidatorUpdateApps, GetUsersValidatorSelectedUnSelectedApps, GetUsersValidatorUpdateApps,  UpdateUserValidatorIn, UserInfoValidator, UserSPPracticeRoleValidatorOut, UserValidatorIn, UserValidatorOut
from src.apis.v1.validators.common_validators import ErrorResponseValidator, SuccessfulJsonResponseValidator

router = APIRouter(tags=["User-Management"])

@router.get("/user", summary="Get User Information", responses={200:{"model":UserInfoValidator}})
async def get_user_info(user_email_role:RoleVerifierImplemented = Depends(),token: str = Depends(oauth2_scheme),db: Session = Depends(get_db)):
    """
        This api get the user information for profile
    """
    current_user_email = user_email_role.get_user_email()
    resp = UserController(db).get_user_info(user_email=current_user_email)
    return resp


@router.put("/user", summary="Update User Information", responses={201:{"model":UserInfoValidator}}, status_code=201)
async def update_user_info(updateuser:UpdateUserValidatorIn, user_email_role:RoleVerifierImplemented = Depends(), token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """
        This api updates the user information for profile
    """

    current_user_email = user_email_role.get_user_email()
    resp = UserController(db).update_user_info(user_email=current_user_email,user_data=updateuser.dict())
    return resp

@router.get("/user/service-providers/practices/roles", summary="Get All Service Providers With Practices And RolesApi",
            responses={200:{"model":UserSPPracticeRoleValidatorOut,"description":"Succesfully returned service providers with their practices and roles"},})
async def get_practice_roles(user_email_role:RoleVerifierImplemented = Depends(), token: str = Depends(oauth2_scheme),db: Session = Depends(get_db)):
# async def get_practice_roles(db: Session = Depends(get_db)):
    """
        Get All Service Providers Practice Roles
    """
    current_user_email = user_email_role.get_user_email()
    resp = UserController(db).get_sps_practice_roles(current_user_email)
    return resp


@router.post("/user", summary="Create User Api", responses={201:{"model":UserValidatorOut},
            404:{"model":ErrorResponseValidator,"description":"Error Occured when not found"},
            500:{"description":"Internal Server Error","model":ErrorResponseValidator}})
async def create_internal_external_user(user_validator:CreateInternalExternalUserValidatorIn, user_email_role:RoleVerifierImplemented = Depends(), token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """
        Create User
    """
    current_user_email = user_email_role.get_user_email()
    print('Current User: %s' % current_user_email)
    resp = UserController(db).create_user(user_validator.dict(), current_user_email)
    return resp


@router.get("/user/{user_id}/service-providers/practices/roles", summary="Get User Information with practices and roles",
            responses={200:{"model": GetUsersValidatorUpdateApps},404:{"model":ErrorResponseValidator,"description":"Error Occured when not found"}})
async def get_user_practices_roles_by_id(user_id:int, user_email_role:RoleVerifierImplemented = Depends(), token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """
        This api get the user information according to relevant service providers and practices
    """
    current_user_email = user_email_role.get_user_email()
    resp = UserController(db).get_user_practices_roles_by_id(user_email=current_user_email,user_id=user_id)
    return resp

@router.put("/user/{user_id}/service-providers/practices/roles", summary="Update User Information with practices and roles",
            status_code=201,
            responses={ 201:{"model":UserValidatorOut},
                        404:{"model":ErrorResponseValidator,"description":"Error Occured when not found"},
                        500:{"description":"Internal Server Error","model":ErrorResponseValidator}})
async def update_user_practices_roles_by_id(user_id:int,user_validator:CreateInternalExternalUserValidatorIn, user_email_role:RoleVerifierImplemented = Depends(),
                                            token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """
        This api updates the user information according to relevant service providers and practices
    """
    resp = UserController(db).update_user_practices_roles_by_id(user_id=user_id,user_data=user_validator.dict())
    return resp

@router.put("/user/profile-image", summary="Update User Profile Image", responses={201:{"model":SuccessfulJsonResponseValidator}}, status_code=201)
async def update_user_image(image:UploadFile = Form(...), user_email_role:RoleVerifierImplemented = Depends(), token: str = Depends(oauth2_scheme),db: Session = Depends(get_db)):
    """
        This api updates the user information for profile image, uses request.body.file
    """

    current_user_email = user_email_role.get_user_email()
    resp = UserController(db).update_user_image(user_email=current_user_email,data_image=image)
    return resp


@router.get("/user/image", summary="Access User Profile Image using token", responses={302:{"model":SuccessfulJsonResponseValidator}}, status_code=302)
async def get_user_image(user_email_role:RoleVerifierImplemented = Depends(), token: str = Depends(oauth2_scheme),db: Session = Depends(get_db)):
    """
        This api returns the user information for profile image, uses request.body.file
    """

    current_user_email = user_email_role.get_user_email()
    resp = UserController(db).get_user_image(user_email=current_user_email)
    return resp

@router.delete("/user/{user_id}", summary="Delete a user",responses={200:{"description":"Delete a user and all associated applications and it's rights"}})
async def delete_user(user_id:int, user_email_role:RoleVerifierImplemented = Depends(), token: str = Depends(oauth2_scheme),db: Session = Depends(get_db)):
    """
        This api deletes the user app, practices and roles
    """
    user_to_delete = UserController(db).delete_user(user_id)
    return user_to_delete

@router.get("/user/selected/apps/practices/roles", summary="Get User Information with practices and roles",
            responses={200:{"model": GetLogedInUsersValidatorUpdateApps},404:{"model":ErrorResponseValidator,"description":"Error Occured when not found"}})
async def get_user_practices_roles_by_id( user_email_role:RoleVerifierImplemented = Depends(), token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """
        This api get the user information according to relevant service providers and practices
    """
    current_user_email = user_email_role.get_user_email()
    resp = UserController(db).get_loged_in_user_practices_roles_by_id(user_email=current_user_email)
    return resp


@router.get("/user/selected/apps", summary="Get User selected unselected  apps",
            responses={200:{"model": GetUsersValidatorSelectedUnSelectedApps},404:{"model":ErrorResponseValidator,"description":"Error Occured when not found"}})
async def get_user_selected_unselected_apps(user_email_role:RoleVerifierImplemented = Depends(), token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """
        This api get the selected and unselected apps for loged in user
    """
    current_user_email = user_email_role.get_user_email()
    resp = UserController(db).get_user_selected_unselected_apps(user_email=current_user_email)
    return resp
