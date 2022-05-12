from email import message
from os import access
from pydantic import BaseModel, validator

class EmailValidator(BaseModel):
    email: str

    @validator('email')
    def validate(cls, email: str) -> bool:
        return True

class LoginValidator(BaseModel):
    email: str
    password: str
class LogoutValidator(BaseModel):
    access_token: str
    refresh_token: str
class EmailValidatorOut(BaseModel):
    message: str
    verification: bool = True
    roles: list
    email: str

class EmailValidatorError(BaseModel):
    message: str
    verification: bool = False

class LoginValidatorError(BaseModel):
    message: str

class LoginValidatorOut(BaseModel):
    message: str
    access_token: str
    refresh_token: str
    token_type: str
    roles: list

class RefreshTokenValidatorOut(BaseModel):
    message: str
    access_token: str

