from email import message
from pydantic import BaseModel
from typing import List,Dict, Optional, Literal

class RoleValidatorIn(BaseModel):
    role: Literal['internal', 'external'] = 'internal'
class InternalRoleValidator(BaseModel):
    id : int
    name : str
    label : str
    is_active : str
    type_of_user: str

class InternalRoleValidatorOut(BaseModel):
    message: str = "success"
    statuscode: int = 200
    roles: Optional[List[InternalRoleValidator]] = None

class ListSPRolesValidator(BaseModel):
    id: int
    name: str
    is_active: str
    
class SPRolesValidator(BaseModel):
    """
        List SP Roles Validator
    """
    __root__: List[ListSPRolesValidator]