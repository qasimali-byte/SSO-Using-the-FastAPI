from pydantic import BaseModel


class EmailValidator(BaseModel):
    email: str

class LoginValidator(BaseModel):
    email: str
    password: str

class EmailValidatorOut(BaseModel):
    message: str
    verification: bool = True
    roles: list
    email: str

class EmailValidatorError(BaseModel):
    message: str
    verification: bool = False