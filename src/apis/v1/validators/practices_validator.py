from pydantic import BaseModel, validator, typing, Field
from pydantic_sqlalchemy import sqlalchemy_to_pydantic

from src.apis.v1.models.practices_model import practices
from pydantic import BaseModel, Field, typing

# PracticesGeneralValidator = sqlalchemy_to_pydantic(practices)

class PracticesGeneralValidator(BaseModel):
    id:int
    name: str
    region_id: typing.Optional[int]

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
    dr_iq_practice_id: typing.Optional[int]
    region_id: typing.Optional[int]
    is_selected: typing.Optional[bool] = Field(alias='isChecked')

    class Config:
        allow_population_by_field_name = True

        @staticmethod
        def pre_process_config(cls, field: Field):
            if field.name == 'dr_iq_practice_id':
                field.required = False  # Make the field optional during validation
            return field

        @staticmethod
        def post_process_result(cls, result):
            if 'dr_iq_practice_id' in result:
                return result
            else:
                return {k: v for k, v in result.items() if k != 'dr_iq_practice_id'}


 
class LogedInUserSPPracticesValidator(BaseModel):
    id: int
    name: str
    # is_selected: typing.Optional[bool] = Field(alias='isChecked')
    class Config:
        allow_population_by_field_name = True

class ListSPRegionsValidator(BaseModel):
    id: int
    name: str
    region_id: typing.Optional[int]
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


class PracticeValidatorIn(BaseModel):
    """
        Create User Validator
    """
    name: str
    sp_apps_id: int
    practice_region_id: int = None


class PracticeValidatorOut(BaseModel):
    statuscode: int = 201
    message: str = "successfully created practice"

