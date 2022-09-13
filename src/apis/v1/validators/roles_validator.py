from pydantic import BaseModel, Field
from pydantic.typing import List,Dict, Optional, Literal

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



class ListSubRolesValidator(BaseModel):
    id: int
    name: str = Field(alias='label')

    class Config:
        orm_mode = True
    



class SubRolesValidator(BaseModel):
    id: int
    name: str 
    sub_roles: Optional[List[ListSubRolesValidator]]
    


class ListRolesValidator(BaseModel):
    id: int
    name: str = Field(alias='label')
    sub_roles : Optional[List[SubRolesValidator]] = []

    class Config:
        orm_mode = True
        

class RolesValidator(BaseModel):
    roles: Optional[List[ListRolesValidator]] = []
    

class SubRolesValidatorWithOutOrm(BaseModel):
    id: int
    name: str 
    is_selected: Optional[bool] = Field(alias='isSelected')

    class Config:
        allow_population_by_field_name = True
        
class LogedInUserSubRolesValidatorWithOutOrm(BaseModel):
    id: int
    name: str 
    # is_selected: Optional[bool] = Field(alias='isSelected')

    class Config:
        allow_population_by_field_name = True
class ListRolesValidatorWithOutOrm(BaseModel):
    id: int
    name: str
    is_selected: Optional[bool] = Field(alias='isSelected')
    sub_roles : Optional[List[SubRolesValidatorWithOutOrm]] = []

    class Config:
        allow_population_by_field_name = True


class LogedInUserListRolesValidatorWithOutOrm(BaseModel):
    id: int
    name: str
    # is_selected: Optional[bool] = Field(alias='isSelected')
    sub_roles : Optional[List[LogedInUserSubRolesValidatorWithOutOrm]] = []

    class Config:
        allow_population_by_field_name = True


class RolesValidatorWithOutOrm(BaseModel):
    roles: Optional[List[ListRolesValidatorWithOutOrm]] = []

class SPRolesValidator(BaseModel):
    """
        List SP Roles Validator
    """
    __root__: List[ListRolesValidatorWithOutOrm]
    
class LogedInUserSPRolesValidator(BaseModel):
    """
        List SP Roles Validator
    """
    __root__: List[LogedInUserListRolesValidatorWithOutOrm]