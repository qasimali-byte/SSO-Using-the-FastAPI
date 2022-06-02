from fastapi import FastAPI, Request
from src.apis.v1.routes import sps_routes, idp_routes,auth_routes,user_routes,\
     frontend_routes,staticfiles_routes 
from . import settings_by_env
from fastapi_jwt_auth.exceptions import AuthJWTException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles



def create_app():
    app = FastAPI()
    app.mount("/static", StaticFiles(directory="build/static"), name="static")
    origins = ["https://chilly-snakes-throw-58-181-125-118.loca.lt","http://localhost:3000","http://localhost:3001","http://18.134.217.103"]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["GET", "POST", "HEAD", "OPTIONS"],
        allow_headers=["Access-Control-Allow-Headers","Set-Cookie", 'Content-Type', 'Authorization', 'Access-Control-Allow-Origin'],
    )
    app.include_router(staticfiles_routes.router)
    app.include_router(sps_routes.router, prefix="/api/v1")
    app.include_router(idp_routes.router)
    app.include_router(auth_routes.router, prefix="/api/v1")
    app.include_router(user_routes.router, prefix="/api/v1")
    app.include_router(frontend_routes.router)
    


    @app.exception_handler(AuthJWTException)
    def authjwt_exception_handler(request: Request, exc: AuthJWTException):
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.message}
        )
    
    return app

# app = create_app()