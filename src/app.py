from datetime import timedelta
import random
from fastapi import FastAPI
from src.handling_exceptions import registering_exceptions
from src.middleware import registering_middleware
from fastapi.staticfiles import StaticFiles
from src.routes import registering_routes
# from fastapi_redis_session.config import basicConfig

def create_app():
    app = FastAPI()
    app.mount("/static", StaticFiles(directory="build/static"), name="static")
    app.mount("/static", StaticFiles(directory="public/profile_image"), name="profile_image")
    registering_middleware(app)
    registering_routes(app)
    registering_exceptions(app)
    return app