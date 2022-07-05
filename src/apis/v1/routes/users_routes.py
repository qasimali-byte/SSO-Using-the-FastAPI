from src.apis.v1.db.session import engine, get_db
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, Query
from src.apis.v1.controllers.users_controller import UsersController
from src.apis.v1.validators.users_validator import UsersValidatorOut
from ..helpers.auth import AuthJWT
from . import oauth2_scheme

router = APIRouter(tags=["Display Users"])


<<<<<<< HEAD
@router.get("/users/", summary="Get Users Information",responses={200:{"model":UsersValidatorOut,"description":"Get All the users and their APP permissions"}})
async def get_users(db: Session = Depends(get_db)):
    db_users = UsersController(db).get_users()
    return db_users

=======
@router.get("/users", summary="List Users",responses={200:{"model":UsersValidatorOut,"description":"Get All the users and their APP permissions"}})
async def get_users(authorize: AuthJWT = Depends(), token: str = Depends(oauth2_scheme), limit:int = Query(default=10), offset:int = Query(default=1,gt=0), db: Session = Depends(get_db)):
    """
        List all the users with their products accroding to the user defined role
    """
    authorize.jwt_required()
    user_email = authorize.get_jwt_subject()
    db_users = UsersController(db).get_users(user_email=user_email, page_limit=limit, page_offset=offset)
    return db_users
>>>>>>> bd0e89834c0b9cff5b806c916934852f10bf62dc
