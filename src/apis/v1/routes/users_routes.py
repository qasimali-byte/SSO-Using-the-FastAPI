from src.apis.v1.db.session import engine, get_db
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, Path
from src.apis.v1.controllers.users_controller import UsersController
from src.apis.v1.validators.users_validator import UsersValidatorOut

router = APIRouter(tags=["Users Management"])


@router.get("/users/", summary="Get Users Information",responses={200:{"model":UsersValidatorOut,"description":"Get All the users and their APP permissions"}})
async def get_users(db: Session = Depends(get_db)):
    db_users = UsersController(db).get_users()
    return db_users