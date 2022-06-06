from pydantic import BaseModel, EmailStr, validator, typing
class AdminUserValidator(BaseModel):
    email: str
    password: str


class InternalUserValidator(BaseModel):
    """
        Internal User Validator
    """
    firstname: str
    lastname: str
    email: typing.Optional[EmailStr]
    user_role: typing.Literal['sub-admin', 'practice-admin'] = "Enter sub-admin or practice-admin"
    surgeries_allowed: typing.Optional[list] = None
    audit_log_access_level: typing.Literal['read-only', 'full-access'] = "Enter read-only or full-access"
    apps_allowed: typing.Set = {"ez-analytics","ez-doc","dr-iq","ez-nav","ez-path"}
    active: bool

    @validator('apps_allowed')
    def validate_apps_allowed(cls, v,  **kwargs):
        apps = kwargs['field'].default
        for iteration in v:
            if iteration not in apps:
                raise ValueError(f'Unexpected value only apps allowed are {apps}')


class UserValidatorOut(BaseModel):
    statuscode: int = 201
    message: str = "successfully created user"

class AppsPracticeRoles(BaseModel):
    apps_allowed: typing.Literal["ez-login","ez-analytics","ez-doc","dr-iq","ez-nav","ez-path"]
    practices: typing.Set = {"practice-1","practice-2"}
    practice_role: str
class ExternalUserValidator(BaseModel):
    """
        External User Validator
    """
    firstname: str
    lastname: str
    email: typing.Optional[EmailStr]
    appspracticeroles: typing.List['AppsPracticeRoles']
