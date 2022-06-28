from sys import prefix
from fastapi import FastAPI, Request
from src.apis.v1.routes import sps_routes, idp_routes,auth_routes,user_routes,\
     frontend_routes,staticfiles_routes, roles_routes, practices_routes, users_routes
from src.handling_exceptions import registering_exceptions
from . import settings_by_env
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles


api_url : str = "/api/v1"

def create_app():
    app = FastAPI()
    app.mount("/static", StaticFiles(directory="build/static"), name="static")
    origins = ["https://chilly-snakes-throw-58-181-125-118.loca.lt","http://localhost:3000","http://localhost:3001","http://18.134.217.103"]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["GET", "POST", "HEAD", "OPTIONS", "PUT", "DELETE"],
        allow_headers=["Access-Control-Allow-Headers","Set-Cookie", 'Content-Type', 'Authorization', 'Access-Control-Allow-Origin'],
    )
    app.include_router(staticfiles_routes.router)
    app.include_router(sps_routes.router, prefix=api_url)
    app.include_router(idp_routes.router)
    app.include_router(auth_routes.router, prefix=api_url)
    app.include_router(user_routes.router, prefix=api_url)
    app.include_router(frontend_routes.router)
    app.include_router(roles_routes.router, prefix=api_url)
    app.include_router(practices_routes.router, prefix=api_url)
    app.include_router(users_routes.router,prefix=api_url)

    registering_exceptions(app)


    
    return app

# app = create_app()