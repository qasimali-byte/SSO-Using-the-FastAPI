from pydantic import BaseModel, validator, typing, Field

class ListGenderValidator(BaseModel):
    id: int
    name: str
    is_selected: typing.Optional[bool] = Field(alias="isSelected")

    class Config:
        orm_mode =True
        allow_population_by_field_name = True

class GenderValidator(BaseModel):
    gender: typing.Optional[typing.List[ListGenderValidator]]