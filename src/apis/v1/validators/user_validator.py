from datetime import datetime
from pydantic import BaseModel, EmailStr, validator, typing, Field
from src.apis.v1.validators.practices_validator import SPRegionsValidator
from src.apis.v1.validators.roles_validator import RolesValidator, SPRolesValidator
from src.apis.v1.validators.gender_validator import ListGenderValidator
import uuid
from src.apis.v1.utils.auth_utils import create_password_hash

class AdminUserValidator(BaseModel):
    email: str
    password: str

class IdsList(BaseModel):
    id: int
class UserRolesValidatorIn(BaseModel):
    id: int
    sub_role: typing.Optional[int] = None
class UserAppsValidatorIn(BaseModel):
    id: int
    practices: typing.List[IdsList] = []
    role: UserRolesValidatorIn

class CreateInternalExternalUserValidatorIn(BaseModel):
    """
        Create User Validator
    """
    firstname: str 
    lastname: str 
    email: EmailStr
    type_of_user: typing.Literal['internal','external']
    dr_iq_gender_id: typing.Optional[int] = None
    apps: typing.List[UserAppsValidatorIn]
    is_active: typing.Optional[bool] = True

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

class SPPracticeRoleValidator(BaseModel):
    """
        SP Practice Role Validator
    """
    id: int
    name: str
    gender: typing.Optional[typing.List[ListGenderValidator]] = []
    sp_app_name: str
    sp_app_image: str
    practices: SPRegionsValidator = []
    roles: typing.Optional[SPRolesValidator]
    is_selected: typing.Optional[bool] = Field(alias='selected')
    
    class Config:
        allow_population_by_field_name = True
        validate_assignment = True

class UserSPPracticeRoleValidatorOut(BaseModel):
    sp_practice_roles: typing.List['SPPracticeRoleValidator']
    message: str = "successfully fetched sp practice roles"
    statuscode: int = 200

class GetUsersValidatorUpdateApps(UserSPPracticeRoleValidatorOut):
    firstname: str 
    lastname: str 
    email: EmailStr
    type_of_user: typing.Literal['internal','external']
    is_active: typing.Optional[bool] 

class PracticesRolesId(BaseModel):
    practice_id: int
    role_id: int
class PracticesAppsRolesValidator(BaseModel):
    """
        Practices Apps Roles Validator
    """
    app: typing.Literal["ez-login","ez-analytics","ez-doc","dr-iq","ez-nav","ez-path"]
    practices_roles: typing.List['PracticesRolesId']
class UserValidatorIn(BaseModel):
    """
        User Validator
    """
    firstname: str
    lastname: str
    email: typing.Optional[EmailStr]
    type_of_user: typing.Literal[ 'external','internal']
    practices_apps_roles: typing.List['PracticesAppsRolesValidator']



class GetUserInfoValidator(BaseModel):
    firstname: str = Field(alias="first_name")
    lastname: str = Field(alias="last_name")
    email: str
    phone_number: str = Field(alias="contact_no")
    address: str = Field(alias="address")
    image_url: typing.Optional[str] = Field(alias="profile_image")

    class Config:
        orm_mode = True


class UserInfoValidator(BaseModel):
    user_info: GetUserInfoValidator
    statuscode: int 
    message: str 


class UpdateUserValidatorIn(BaseModel):
    first_name: str = Field(alias="first_name")
    last_name: str = Field(alias="last_name")
    contact_no: str = Field(alias="contact_no")
    address: str = Field(alias="address")

class CreateUserValidator(BaseModel):
        uuid : uuid.UUID
        first_name: str = Field(alias="firstname")
        last_name: str = Field(alias="lastname")
        username : str
        email : EmailStr
        nhs_number = "123456789"
        organization_id = "2"
        contact_no = "+92123456789"
        address = "enter address here"
        password_hash = create_password_hash("admin")
        reset_password_token = 'reset_password_token',
        reset_password_token_expiry = 'reset_password_token_expiry',
        profile_image = "image/profile_image.jpg"
        created_date = datetime.now(),
        updated_date = datetime.now(),
        last_login_date = datetime.now()
        user_type_id: int
        dr_iq_gender_id: typing.Optional[int]
        is_active: bool = True

        class Config:
            arbitrary_types_allowed = True

class UserDeleteValidatorOut(BaseModel):
    message: str
    status_code: int
    class Config:
        orm_mode = True 
class UpdateUserValidatorDataClass(BaseModel):
    first_name: str = Field(alias="firstname")
    last_name: str = Field(alias="lastname")
    username : str
    updated_date : datetime
    user_type_id: int
    dr_iq_gender_id: typing.Optional[int]
    is_active: bool = True
