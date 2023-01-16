from datetime import datetime
from pydantic import BaseModel, EmailStr, validator, typing, Field
from src.apis.v1.validators.practices_validator import LogedInUserSPRegionsValidator, SPRegionsValidator
from src.apis.v1.validators.roles_validator import LogedInUserListRolesValidatorWithOutOrm,  RolesValidator, SPRolesValidator
from src.apis.v1.validators.gender_validator import ListGenderValidator, LogedInUserListGenderValidator
import uuid
from src.apis.v1.utils.auth_utils import create_password_hash, generate_password


class AdminUserValidator(BaseModel):
    email: str
    password: str

    @validator('email')
    def validate_email(cls, v):
        return v.lower()
class ForgetPasswordValidator(BaseModel):
    email: str

    @validator('email')
    def validate_email(cls, v):
        return v.lower()

class SetPasswordValidator(BaseModel):
    password: str


class ChangePasswordValidator(BaseModel):
    old_password: str


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

    @validator('email')
    def validate_email(cls, v):
        return v.lower()

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

    @validator('email')
    def validate_email(cls, v):
        return v.lower()
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



class UserSelectedUnselectedSPApps(BaseModel):
    """
        SP Apps Validator
    """
    id: int
    name: str
    sp_app_name: str
    logo_url: str
    host_url: str
    is_selected: typing.Optional[bool]
    
    class Config:
        allow_population_by_field_name = True
        validate_assignment = True




class LogedInUserSPPracticeRoleValidator(BaseModel):
    """
        SP Practice Role Validator
    """
    id: int
    name: str
    gender: typing.Optional[LogedInUserListGenderValidator]
    sp_app_name: str
    sp_app_image: str
    practices: LogedInUserSPRegionsValidator = []
    role: typing.Optional[LogedInUserListRolesValidatorWithOutOrm]
    # is_selected: typing.Optional[bool] = Field(alias='selected')
    
    class Config:
        allow_population_by_field_name = True
        validate_assignment = True

class UserSPPracticeRoleValidatorOut(BaseModel):
    sp_practice_roles: typing.List['SPPracticeRoleValidator']
    message: str = "successfully fetched sp practice roles"
    statuscode: int = 200
    

class LogedInUserSPPracticeRoleValidatorOut(BaseModel):
    sp_practice_roles: typing.List['LogedInUserSPPracticeRoleValidator']
    message: str = "successfully fetched sp practice roles"
    statuscode: int = 200

class GetUsersValidatorUpdateApps(UserSPPracticeRoleValidatorOut):
    firstname: str 
    lastname: str 
    email: EmailStr
    type_of_user: typing.Literal['internal','external']
    is_active: typing.Optional[bool] 

    @validator('email')
    def validate_email(cls, v):
        return v.lower()




class UserSelectedSPAppsValidatorOut(BaseModel):
    selected_unselected_sp_apps: typing.List['UserSelectedUnselectedSPApps']
    message: str = "successfully fetched sp apps"
    statuscode: int = 200


class GetUsersValidatorSelectedUnSelectedApps(UserSelectedSPAppsValidatorOut):
    firstname: str 
    lastname: str 
    email: EmailStr
    type_of_user: typing.Literal['internal','external']
    is_active: typing.Optional[bool] 

    @validator('email')
    def validate_email(cls, v):
        return v.lower()



    
class GetLogedInUsersValidatorUpdateApps(LogedInUserSPPracticeRoleValidatorOut):
    firstname: str 
    lastname: str 
    email: EmailStr
    type_of_user: typing.Literal['internal','external']
    is_active: typing.Optional[bool] 

    @validator('email')
    def validate_email(cls, v):
        return v.lower()

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

    @validator('email')
    def validate_email(cls, v):
        return v.lower()


class GetUserInfoValidator(BaseModel):
    firstname: str = Field(alias="first_name")
    lastname: str = Field(alias="last_name")
    email: str
    phone_number: str = Field(alias="contact_no")
    address: str = Field(alias="address")
    image_url: typing.Optional[str] = Field(alias="profile_image")

    @validator('email')
    def validate_email(cls, v):
        return v.lower()

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
    nhs_number: str = "0"
    organization_id = "2"
    contact_no: str = None
    address = "enter address here"
    password_hash = create_password_hash("admin")
    reset_password_token = 'reset_password_token',
    reset_password_token_expiry = 'reset_password_token_expiry',
    profile_image = "image/profile_image.jpg"
    created_date: datetime = Field(default_factory=datetime.now)
    created_by: str = None
    updated_date: datetime = Field(default_factory=datetime.now)
    last_login_date: datetime = Field(default_factory=datetime.now)
    user_type_id: int
    dr_iq_gender_id: typing.Optional[int]
    is_active: bool = False


    @validator('email')
    def validate_email(cls, v):
        return v.lower()

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
