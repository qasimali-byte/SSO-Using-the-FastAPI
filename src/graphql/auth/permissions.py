import typing
from fastapi import HTTPException, Request, WebSocket
from strawberry.permission import BasePermission
from strawberry.types import Info
from src.apis.v1.helpers.auth import AuthJWT

class IsAuthenticated(BasePermission):

    # This method can also be async!
    async def has_permission(self, source: typing.Any, info: Info, **kwargs) -> bool:

            request: Request = info.context["request"]
            authorize=AuthJWT(request)
            authorize.jwt_required()
            return True