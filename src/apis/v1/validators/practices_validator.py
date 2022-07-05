from pydantic import BaseModel, validator, typing, Field

class SPPracticesValidator(BaseModel):
    id: int
    name: str
    is_selected: typing.Optional[bool] = Field(alias='isChecked')
    class Config:
        allow_population_by_field_name = True

class ListSPRegionsValidator(BaseModel):
    id: int
    name: str
    is_selected: typing.Optional[bool] = Field(alias='isChecked')
    practices: typing.List[SPPracticesValidator]
    class Config:
        allow_population_by_field_name = True
        
class SPRegionsValidator(BaseModel):
    """
        List SP Practices Validator
    """
    __root__: typing.List[ListSPRegionsValidator]