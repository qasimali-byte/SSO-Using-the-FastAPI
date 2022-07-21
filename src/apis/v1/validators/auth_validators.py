from pydantic import BaseModel, validator, EmailStr
from typing import Optional

class EmailValidator(BaseModel):
    email: str

    @validator('email')
    def validate(cls, email: str) -> bool:
        return True

class LoginValidator(BaseModel):
    email: Optional[EmailStr]
    password: str
    
class LogoutValidator(BaseModel):
    access_token: str
    refresh_token: str
    
class EmailValidatorOut(BaseModel):
    message: str
    verification: bool = True
    roles: list
    email: str
    statuscode: int

class EmailValidatorError(BaseModel):
    message: str
    verification: bool = False
    statuscode: int

class LoginValidatorError(BaseModel):
    message: str
    statuscode: int

class LoginValidatorOut(BaseModel):
    product_name: str
    message: str
    access_token: str
    refresh_token: str
    token_type: str
    roles: list
    statuscode: int

class LoginValidatorOutRedirect(BaseModel):
    product_name: str
    redirect_url: str
    saml_response: str
    message: str
    access_token: str
    refresh_token: str
    token_type: str
    roles: list
    statuscode: int

class RefreshTokenValidatorOut(BaseModel):
    message: str
    access_token: str
    statuscode: int

