from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
templates = Jinja2Templates(directory="build")


router = APIRouter(tags=["SSO Frontend"])

@router.get("/")
async def serve_spa(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@router.get("/sign-in")
async def serve_spa(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})