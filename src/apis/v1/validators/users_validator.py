from enum import Enum

from pydantic import BaseModel, Field, typing
from src.apis.v1.validators.common_validators import MetaDataValidator


class UsersValidator(BaseModel):
    first_name: str 
    last_name: str
    id: int
    email: str
    products: list



class UsersValidatorOut(BaseModel):
    metadata: MetaDataValidator = Field(alias="_metadata")
    users_data: typing.List[UsersValidator]
    message: str
    status_code: int

class UserStatus(str, Enum):
    true = "true"
    false = "false"
    all = "all"