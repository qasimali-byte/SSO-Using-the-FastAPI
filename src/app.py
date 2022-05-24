from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from src.apis.v1.routes import sps_routes, idp_routes,auth_routes,user_routes 
from . import settings_by_env
from fastapi_jwt_auth.exceptions import AuthJWTException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

def create_app():
    app = FastAPI()
    origins = ["http://localhost:3000"]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    templates = Jinja2Templates(directory="templates/")
    app.include_router(sps_routes.router, prefix="/api/v1")
    app.include_router(idp_routes.router)
    app.include_router(auth_routes.router, prefix="/api/v1")
    app.include_router(user_routes.router, prefix="/api/v1")

    @app.exception_handler(AuthJWTException)
    def authjwt_exception_handler(request: Request, exc: AuthJWTException):
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.message}
        )
    
    return app

# app = create_app()