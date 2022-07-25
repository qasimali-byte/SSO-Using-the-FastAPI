from typing import Optional
import strawberry
from src.graphql.auth.permissions import IsAuthenticated
from src.graphql.constants.enums import ActionLevelEnum, DirectionEnum, RoleEnum
from src.graphql.db.session import get_session

from src.graphql.resolvers.user_action_resolver import get_user_actions
from src.graphql.scalars.pagination_scalar import Connection
from src.graphql.scalars.user_action_scalar import UserAction

Cursor = str
@strawberry.type
class Query:

    @strawberry.field(permission_classes=[IsAuthenticated])
    async def user_actions(self, first: int = 10, cursor: Optional[Cursor] = None, direction: DirectionEnum = "forward",
        search: Optional[str] = None,user_id: Optional[int] = None, role_name: Optional[RoleEnum] = None,action_level: Optional[ActionLevelEnum]=None,
        start_date_time:Optional[str]=None,end_date_time:Optional[str]=None) -> Connection[UserAction]:
        
        async with get_session() as s:
            return await get_user_actions(db=s,first=first,cursor=cursor,direction=direction,search=search,user_id=user_id,
            role_name=role_name,action_level=action_level,start_date_time=start_date_time,end_date_time=end_date_time) 