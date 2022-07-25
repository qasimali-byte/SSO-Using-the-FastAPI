from src.apis.v1.middleware.middleware import AddActionMiddleWare
from src.apis.v1.middleware.middleware import AddActionMiddleWare
from src.apis.v1.constants.origins_enum import origins
from fastapi.middleware.cors import CORSMiddleware

def registering_middleware(application):
    application.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["GET", "POST", "HEAD", "OPTIONS", "PUT", "DELETE"],
        allow_headers=["Access-Control-Allow-Headers","Set-Cookie", 'Content-Type', 'Authorization', 'Access-Control-Allow-Origin'],
    )
    application.add_middleware(AddActionMiddleWare)