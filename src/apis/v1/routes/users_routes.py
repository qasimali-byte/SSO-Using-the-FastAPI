from email.policy import default
from sqlalchemy import asc
from src.apis.v1.db.session import engine, get_db
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, Query
from src.apis.v1.controllers.users_controller import UsersController
from src.apis.v1.helpers.role_verifier import RoleVerifierImplemented
from src.apis.v1.validators.users_validator import UsersValidatorOut, UserStatus
from ..helpers.auth import AuthJWT
from . import oauth2_scheme

router = APIRouter(tags=["Display Users"])


@router.get("/users", summary="List Users",responses={200:{"model":UsersValidatorOut,"description":"Get All the users and their APP permissions"}})
async def get_users(user_email_role:RoleVerifierImplemented = Depends(), token: str = Depends(oauth2_scheme),limit:int = Query(default=10), offset:int = Query(default=1,gt=0), db: Session = Depends(get_db),order_by:str = Query(default='id'),\
    latest:bool =Query(default=True),status : UserStatus=UserStatus.all ,search:str = Query(default=None),practices:list =Query(default=['All'])):
    """
        List all the users with their products accroding to the user defined role
    """
    user_role = user_email_role.get_user_role()
    db_users = UsersController(db).get_users(user_role=user_role, page_limit=limit, page_offset=offset,order_by=order_by,latest=latest,\
        search=search,user_status=status,select_practices=practices)
    return db_users
