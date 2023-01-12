from fastapi import APIRouter, Depends, Path
from pydantic import ValidationError
from src.apis.v1.helpers.customize_response import custom_response
from src.apis.v1.constants.role_enums import RoleEnums
from src.apis.v1.validators.common_validators import ErrorResponseValidator
from src.apis.v1.db.session import engine, get_db
from sqlalchemy.orm import Session
from ..helpers.auth import AuthJWT

from src.apis.v1.validators.roles_validator import InternalRoleValidatorIn, InternalRoleValidatorOut, RoleValidatorIn, RoleAPIValidatorIn, RoleAPIValidatorOut
from . import oauth2_scheme

from src.apis.v1.controllers.roles_controller import RolesController

router = APIRouter(tags=["Roles"])

@router.get("/roles/{role}", summary="Get Roles",
            responses={200:{"model":InternalRoleValidatorOut,"description":"succesfully returned roles"},
            404:{"model":ErrorResponseValidator,"description":"role not found"},
            500:{"description":"Internal Server Error","model":ErrorResponseValidator},
            })
async def get_roles(authorize: AuthJWT = Depends(), token: str = Depends(oauth2_scheme),
                    role:RoleEnums= Path(title="the role to get",default="internal"), db: Session = Depends(get_db)):
    """
        Get Internal And External Roles
    """

    authorize.jwt_required()
    if role.value == "internal":
        return RolesController(db).internal_roles()

    elif role.value == "external":
        return RolesController(db).external_roles()

    else:
        return custom_response({"message": "Invalid Role"}, status_code=404)


@router.post("/role_api", summary="Create a role_api", responses={201: {"model": RoleAPIValidatorOut}, 500: {"description": "Internal Server Error", "model": ErrorResponseValidator}})
async def create_role_api(role_api_validator: RoleAPIValidatorIn, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """
        Create role_api
    """
    resp = RolesController(db).create_role_api(role_api_validator.dict())
    return resp


@router.delete("/role_api/{role_api_id}", summary="Delete a role_api",responses={200:{"description": "successfully deleted role_api"}})
async def delete_role_api(role_api_id:int, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """
        This api deletes the role_api
    """
    role_to_delete = RolesController(db).delete_role_api(role_api_id)
    return role_to_delete


@router.post("/role", summary="Create a role", responses={201: {"description":"successfully created a role"},404: {"model": ErrorResponseValidator, "description": "Error Occurred when not found"}, 500: {"description": "Internal Server Error", "model": ErrorResponseValidator}})
async def create_role(role_validator: InternalRoleValidatorIn, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """
        Create Role
    """
    resp = RolesController(db).create_role(role_validator.dict())
    return resp


@router.delete("/role/{role_id}", summary="Delete a role", responses={200:{"description":"successfully deleted role"}})
async def delete_role(role_id:int, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """
        This api deletes a role and associated users
    """
    role_to_delete = RolesController(db).delete_role(role_id)
    return role_to_delete
