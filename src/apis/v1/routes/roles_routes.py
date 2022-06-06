from fastapi import APIRouter, Depends
from src.apis.v1.validators.common_validators import ErrorResponseValidator
from src.apis.v1.db.session import engine, get_db
from sqlalchemy.orm import Session
from fastapi_jwt_auth import AuthJWT

from src.apis.v1.validators.roles_validator import InternalRoleValidatorOut
from . import oauth2_scheme

from src.apis.v1.controllers.roles_controller import RolesController

router = APIRouter(tags=["Roles"])

@router.get("/roles/internal", summary="Get Internal Roles",
            responses={200:{"model":InternalRoleValidatorOut,"description":"succesfully returned internal roles"},
            500:{"description":"Internal Server Error","model":ErrorResponseValidator},
            })
async def get_internal_roles(authorize: AuthJWT = Depends(), token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """
        Get Internal Roles
    """
    authorize.jwt_required()
    resp = RolesController(db).internal_roles()
    return resp