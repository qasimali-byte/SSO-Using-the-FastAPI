from fastapi import FastAPI
from src.handling_exceptions import registering_exceptions
from src.middleware import registering_middleware
from fastapi.staticfiles import StaticFiles
from src.routes import registering_routes

def create_app():
    app = FastAPI()
    app.mount("/static", StaticFiles(directory="build/static"), name="static")
    registering_middleware(app)
    registering_routes(app)
    registering_exceptions(app)
    return app