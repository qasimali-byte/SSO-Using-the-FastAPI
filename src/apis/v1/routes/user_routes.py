from datetime import datetime
from uuid import uuid4
from fastapi import Depends, HTTPException, Request, APIRouter, Response
from src.apis.v1.services.auth_service import AuthService
from src.apis.v1.core.project_settings import Settings
from src.apis.v1.controllers.auth_controller import AuthController
from src.apis.v1.db.session import engine, get_db
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from src.apis.v1.validators.user_validators import AdminUserValidator, InternalUserValidator
from src.apis.v1.utils.auth_utils import create_password_hash



router = APIRouter(tags=["User-Management"])


@router.post("/user/admin", summary="Create Admin User Api")
async def create_user(user_validator:AdminUserValidator,request: Request,db: Session = Depends(get_db)):
    """
        Create Admin User 
    """
    pass

@router.post("/user/internal", summary="Create Internal User Api")
async def create_user(user_validator:InternalUserValidator,request: Request,db: Session = Depends(get_db)):
    """
        Create Internal User 
    """
    pass
