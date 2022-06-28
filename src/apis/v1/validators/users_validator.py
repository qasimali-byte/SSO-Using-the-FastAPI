from pydantic import BaseModel, typing, Field
from src.apis.v1.models import user_idp_sp_apps_model


class UsersValidator(BaseModel):
    first_name: str 
    last_name: str
    id: int
    email: str
    products: list



class UsersValidatorOut(BaseModel):
    users_data: typing.List[UsersValidator]
    message: str
    status_code: int

    