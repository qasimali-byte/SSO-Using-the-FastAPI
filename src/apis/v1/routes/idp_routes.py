from fastapi import Depends, Form, Request, APIRouter, Response
from src.apis.v1.db.session import engine, get_db
from sqlalchemy.orm import Session

router = APIRouter(tags=["Identity Provider"])

@router.get("/sso/redirect/",summary="Only Redirect Request from Service Provider")
async def sso_redirect(request: Request, SAMLRequest: str,db: Session = Depends(get_db)):
    pass

@router.post("/sso/login", summary="Submit Login Page API submission")
async def sso_login(response: Response,request: Request,email: str = Form(...),password: str = Form(...),saml_request: str = Form(...),db: Session = Depends(get_db)):
    pass

@router.get("/sso/logout",summary="Logout Request API From Service Provider")
async def sso_logout(request: Request,response : Response,SAMLRequest: str,db: Session = Depends(get_db)):
    pass