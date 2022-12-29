from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from src.apis.v1.helpers.auth import AuthJWT
from src.apis.v1.helpers.global_helpers import remove_int_from_urls
from src.apis.v1.utils.middleware_utils import store_logs_db

class AddActionMiddleWare(BaseHTTPMiddleware):
    def __init__(
            self,
            app,
    ):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next):
        # do something with the request object, for example
        authorize=AuthJWT(request)

        method = request.method
        url = request.url.path
        url = remove_int_from_urls(url)
        response = await call_next(request)

        ### code after response of api
        await store_logs_db(authorize,response,method,url)

        return response