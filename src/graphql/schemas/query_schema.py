from typing import Optional
import strawberry
from src.graphql.auth.permissions import IsAuthenticated
from src.graphql.constants.enums import ActionLevelEnum, DirectionEnum, RoleEnum
from src.graphql.db.session import get_session

from src.graphql.resolvers.user_action_resolver import get_user_actions
from src.graphql.scalars.pagination_scalar import Connection
from src.graphql.scalars.user_action_scalar import UserAction
from strawberry.types import Info

Cursor = str
@strawberry.type
class Query:

    @strawberry.field
    async def user_actions(self, info:Info, first: int = 10, cursor: Optional[Cursor] = None, direction: DirectionEnum = "forward",
        search: Optional[str] = None,user_email: Optional[str] = None, role_name: Optional[RoleEnum] = None,action_level: Optional[ActionLevelEnum]='user',
        start_date_time:Optional[str]=None,end_date_time:Optional[str]=None) -> Connection[UserAction]:
        

        IsAuthenticated().has_permission(action_level,info)
        async with get_session() as s:

                return await get_user_actions(db=s,first=first,cursor=cursor,direction=direction,search=search,user_email=user_email,
                role_name=role_name,action_level=action_level,start_date_time=start_date_time,end_date_time=end_date_time) 