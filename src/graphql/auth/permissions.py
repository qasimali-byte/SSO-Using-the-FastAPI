from contextlib import contextmanager
import typing
from fastapi import HTTPException, Request, WebSocket
from strawberry.types import Info
from src.apis.v1.db.session import get_db
from src.apis.v1.helpers.role_verifier import ApiUrl, AuthorizeUserRole
from src.apis.v1.utils.auth_utils import auth_jwt_verifier_and_get_subject
from src.packages.roles_authorizer.role_authorizer import RoleVerifier

class StrawberryBasePermission:
    """
    Base class for creating permissions
    """

    message: typing.Optional[str] = None

    def has_permission(
        self
    ) :
        raise NotImplementedError(
            "Permission classes should override has_permission method"
        )

class GraphQLRoleAuthorizer(RoleVerifier):

    def __init__(self, action_level, current_user_email, method,url) -> None:
        self.action_level = action_level
        self.current_user_email = current_user_email
        self.method = method
        self.url = url

    def verify(self):
        if self.action_level == "application" or self.action_level == None:
            with contextmanager(get_db)() as session:  # execute until yield. Session is yielded value
                db = session
                try:
                    authorize_object = AuthorizeUserRole(db, self.current_user_email, self.method, self.url)
                    authorize_object()
                except HTTPException:
                    raise Exception("not enough privileges to perform an action on a resource")
class IsAuthenticated(StrawberryBasePermission):

    def has_permission(self, action_level:str, info: Info) -> bool:

        request: typing.Union[Request, WebSocket] = info.context["request"]
        
        current_user_email = auth_jwt_verifier_and_get_subject(request)
        api_method_url = ApiUrl(request)

        method,url = api_method_url
        GraphQLRoleAuthorizer(action_level,current_user_email,method,url)

        return True