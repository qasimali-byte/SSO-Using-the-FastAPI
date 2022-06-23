from fastapi import APIRouter, Depends, Path
from pydantic import ValidationError
from src.apis.v1.helpers.customize_response import custom_response
from src.apis.v1.constants.role_enums import RoleEnums
from src.apis.v1.validators.common_validators import ErrorResponseValidator
from src.apis.v1.db.session import engine, get_db
from sqlalchemy.orm import Session
from fastapi_auth.auth import AuthJWT

from src.apis.v1.validators.roles_validator import InternalRoleValidatorOut, RoleValidatorIn
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