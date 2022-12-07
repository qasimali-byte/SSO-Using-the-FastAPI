<<<<<<< HEAD
from src.apis.v1.middleware.middleware import AddActionMiddleWare, SecurityHeadersMiddleware
from src.apis.v1.constants.origins_enum import origins
from fastapi.middleware.cors import CORSMiddleware

=======
from src.apis.v1.middleware.middleware import AddActionMiddleWare
from src.apis.v1.constants.origins_enum import origins
from fastapi.middleware.cors import CORSMiddleware
>>>>>>> 3d6d1277ab41be7d23c06f1c549d506a5cff47f6





def registering_middleware(application):
    application.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["GET", "POST", "HEAD", "OPTIONS", "PUT", "DELETE"],
        allow_headers=["Access-Control-Allow-Headers","Set-Cookie", 'Content-Type', 'Authorization', 'Access-Control-Allow-Origin'],
    )
<<<<<<< HEAD
    
=======
>>>>>>> 3d6d1277ab41be7d23c06f1c549d506a5cff47f6
    application.add_middleware(AddActionMiddleWare)
    application.add_middleware(SecurityHeadersMiddleware, csp=True)
    