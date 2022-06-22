from pydantic import BaseModel, validator, typing

class ListGenderValidator(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode =True

class GenderValidator(BaseModel):
    gender: typing.Optional[typing.List[ListGenderValidator]]