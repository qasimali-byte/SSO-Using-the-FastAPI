from pydantic import BaseModel, typing, Field

class TypeOfUserValidator(BaseModel):
    """
        Type Of User Validator
    """
    id: int
    name: typing.Literal['external','internal'] = Field(alias="user_type")

    class Config:
        orm_mode = True