from pydantic import BaseModel, Field
from pydantic.typing import List,Dict, Optional, Literal

class RoleValidatorIn(BaseModel):
    role: Literal['internal', 'external'] = 'internal'
class InternalRoleValidatorIn(BaseModel):
    name : str
    label : str
    is_active : bool = True
    user_type_id: int = 1

class InternalRoleValidatorOut(BaseModel):
    message: str = "success"
    statuscode: int = 200
    roles: Optional[List[InternalRoleValidatorIn]] = None

class ListSPRolesValidator(BaseModel):
    id: int
    name: str

class ListSubRolesValidator(BaseModel):
    id: int
    name: str = Field(alias='label')
    dr_iq_practice_role_id: int

    class Config:
        orm_mode = True

class SubRolesValidator(BaseModel):
    id: int
    name: str
    dr_iq_role_id: Optional[int]
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
    dr_iq_practice_role_id: Optional[int]
    is_selected: Optional[bool] = Field(alias='isSelected')

    class Config:
        allow_population_by_field_name = True
        
class LogedInUserSubRolesValidatorWithOutOrm(BaseModel):
    id: Optional[int]
    name: Optional[str]
    # is_selected: Optional[bool] = Field(alias='isSelected')

    class Config:
        allow_population_by_field_name = True
from typing import List, Optional
from pydantic import BaseModel, Field

class ListRolesValidatorWithOutOrm(BaseModel):
    id: int
    name: str
    dr_iq_role_id: Optional[int]
    is_selected: Optional[bool] = Field(alias='isSelected')
    sub_roles: Optional[List[SubRolesValidatorWithOutOrm]] = []

    class Config:
        allow_population_by_field_name = True

    @classmethod
    def from_orm(cls, obj):
        model_dict = obj.__dict__
        if 'dr_iq_role_id' not in model_dict:
            model_dict.pop('dr_iq_role_id', None)
        return cls(**model_dict)


    class Config:
        allow_population_by_field_name = True


class LogedInUserListRolesValidatorWithOutOrm(BaseModel):
    id: Optional[int]
    name: Optional[str]
    # is_selected: Optional[bool] = Field(alias='isSelected')
    sub_role : Optional[LogedInUserSubRolesValidatorWithOutOrm] = None

    class Config:
        allow_population_by_field_name = True


class RolesValidatorWithOutOrm(BaseModel):
    roles: Optional[List[ListRolesValidatorWithOutOrm]] = []

class SPRolesValidator(BaseModel):
    """
        List SP Roles Validator
    """
    __root__: List[ListRolesValidatorWithOutOrm]
    

class RoleAPIValidatorIn(BaseModel):
    """
        Create User Validator
    """
    role_id: int
    api_id: int
    is_allowed: bool = False


class RoleAPIValidatorOut(BaseModel):
    statuscode: int = 201
    message: str = "successfully created a role_api"


class RoleAPIDeleteValidatorOut(BaseModel):
    message: str
    status_code: int

    class Config:
        orm_mode = True


