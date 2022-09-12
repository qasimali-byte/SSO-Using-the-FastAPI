from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
templates = Jinja2Templates(directory="build")
templates2 = Jinja2Templates(directory="templates")

router = APIRouter(tags=["SSO Frontend"], include_in_schema=False)

@router.get("/")
@router.get("/sign-in")
@router.get("/user-management")
@router.get("/forgot-password")
@router.get("/audit-trail")
@router.get("/create-user")
@router.get("/reset-password")
@router.get("/home")
async def serve_spa(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@router.get("/backend/notification")
@router.post("/backend/notification")
async def serve_notification_page(request: Request):
    return templates2.TemplateResponse("notification.html", {"request": request})
