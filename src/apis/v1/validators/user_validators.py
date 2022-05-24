from pydantic import BaseModel, validator

class AdminUserValidator(BaseModel):
    email: str
    password: str

class InternalUserValidator(BaseModel):
    user_role: str
    surgeries_allowed: list
    audit_log_access_level: str
    apps_allowed: list
    active: bool

    @validator('user_role')
    def validate_user_role(cls, v):
        if v not in ['sub-admin', 'practice admin']:
            raise ValueError('Invalid user_role')
        return v

    @validator('apps_allowed')
    def validate_apps_allowed(cls, v):
        apps = {"ez-analytics","ez-docs","dr-iq","ez-nav"}
        for iteration in v:
            if iteration not in apps:
                raise ValueError('Invalid apps in query')
    