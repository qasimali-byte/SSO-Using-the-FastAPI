from datetime import datetime
from uuid import uuid4
from fastapi import Depends, HTTPException, Request, APIRouter, Response
from src.apis.v1.controllers.user_controller import UsersController
from src.apis.v1.services.auth_service import AuthService
from src.apis.v1.core.project_settings import Settings
from src.apis.v1.controllers.auth_controller import AuthController
from src.apis.v1.db.session import engine, get_db
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from src.apis.v1.validators.user_validators import AdminUserValidator, ExternalUserValidator, InternalUserValidator, UserValidatorOut
from src.apis.v1.utils.auth_utils import create_password_hash



router = APIRouter(tags=["User-Management"])


@router.post("/user/admin", summary="Create Admin User Api")
async def create_user(user_validator:AdminUserValidator,request: Request,db: Session = Depends(get_db)):
    """
        Create Admin User 
    """
    pass

@router.post("/user/internal", summary="Create Internal User Api", responses={201:{"model":UserValidatorOut}})
async def create_internal_user(user_validator:InternalUserValidator,request: Request,db: Session = Depends(get_db)):
    """
        Create Internal User 
    """
    req = await request.json()
    UsersController(db).create_internal_user()
    pass

@router.post("/user/external", summary="Create External User Api", responses={201:{"model":UserValidatorOut}})
async def create_external_user(user_validator:ExternalUserValidator,request: Request,db: Session = Depends(get_db)):
    """
        Create External User 
    """
    req = await request.json()
    pass