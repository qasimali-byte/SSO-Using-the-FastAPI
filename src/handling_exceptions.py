from src.apis.v1.helpers.custom_exceptions import CustomException
from fastapi_jwt_auth.exceptions import AuthJWTException
from fastapi.responses import JSONResponse
from fastapi.requests import Request
from fastapi.encoders import jsonable_encoder

def registering_exceptions(application):

    
    @application.exception_handler(CustomException)
    async def server_error(request: Request, exec: CustomException):
        return JSONResponse(
            status_code=exec.status_code,
            content=jsonable_encoder({"statuscode": exec.status_code, "message": exec.message})
        )

    @application.exception_handler(AuthJWTException)
    def authjwt_exception_handler(request: Request, exc: AuthJWTException):
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.message}
        )