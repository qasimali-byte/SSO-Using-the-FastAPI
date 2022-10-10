from pydantic import BaseModel, validator, typing, Field
from pydantic_sqlalchemy import sqlalchemy_to_pydantic

from src.apis.v1.models.practices_model import practices

# PracticesGeneralValidator = sqlalchemy_to_pydantic(practices)

class PracticesGeneralValidator(BaseModel):
    id:int
    name: str

    # @validator('name')
    # def change_name_lower(cls,name):
    #   return name.lower()
    class Config:
        orm_mode = True 
class ListPracticesGeneralValidator(BaseModel):
    __root__: typing.List[PracticesGeneralValidator]
    class Config:
        orm_mode = True 
class SPPracticesValidator(BaseModel):
    id: int
    name: str
    is_selected: typing.Optional[bool] = Field(alias='isChecked')
    class Config:
        allow_population_by_field_name = True
        
class LogedInUserSPPracticesValidator(BaseModel):
    id: int
    name: str
    # is_selected: typing.Optional[bool] = Field(alias='isChecked')
    class Config:
        allow_population_by_field_name = True

class ListSPRegionsValidator(BaseModel):
    id: int
    name: str
    is_selected: typing.Optional[bool] = Field(alias='isChecked')
    practices: typing.List[SPPracticesValidator]
    class Config:
        allow_population_by_field_name = True
  

class LogedInUserListSPRegionsValidator(BaseModel):
    id: int
    name: str
    # is_selected: typing.Optional[bool] = Field(alias='isChecked')
    practices: typing.List[LogedInUserSPPracticesValidator]
    class Config:
        allow_population_by_field_name = True

      
class SPRegionsValidator(BaseModel):
    """
        List SP Practices Validator
    """
    __root__: typing.List[ListSPRegionsValidator]
    
    
class LogedInUserSPRegionsValidator(BaseModel):
    """
        List SP Practices Validator
    """
    __root__: typing.List[LogedInUserListSPRegionsValidator]