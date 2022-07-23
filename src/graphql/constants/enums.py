from enum import Enum

import strawberry

@strawberry.enum
class DirectionEnum(str,Enum):
    forward = "forward"
    backward = "backward"

@strawberry.enum
class RoleEnum(str,Enum):
    super_admin = "super-admin"
    sub_admin = "sub-admin"
    practice_admin = "practice-admin"

@strawberry.enum
class ActionLevelEnum(str,Enum):
    user = "user"
    application = "application"