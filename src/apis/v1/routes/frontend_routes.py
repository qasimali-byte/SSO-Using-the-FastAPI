from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
templates = Jinja2Templates(directory="build")


router = APIRouter(tags=["SSO Frontend"], include_in_schema=False)

@router.get("/")
@router.get("/sign-in")
@router.get("/user-managment")
@router.get("/forgot-password")
@router.get("/audit-trail")
@router.get("/create-user")
@router.get("/reset-password")
@router.get("/home")
async def serve_spa(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
