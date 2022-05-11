from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from src.apis.v1.routes import sps_routes, idp_routes,auth_routes 
from . import settings_by_env
def create_app():
    app = FastAPI()
    templates = Jinja2Templates(directory="templates/")
    app.include_router(sps_routes.router, prefix="/api/v1")
    app.include_router(idp_routes.router)
    app.include_router(auth_routes.router, prefix="/api/v1")

    return app

# app = create_app()