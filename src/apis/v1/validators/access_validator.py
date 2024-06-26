from typing import Optional, Union
import typing
from pydantic import BaseModel,EmailStr, Field, validator
from pydantic.class_validators import List
import re
from datetime import datetime

from src.apis.v1.validators.common_validators import MetaDataValidator


class OtpAccountValidator(BaseModel):
    email: EmailStr
    otp: str
    app_id: int


class OtpEmailValidator(BaseModel):
    email: EmailStr
    product_name: str
    product_id:int


class OtpProductsValidator(BaseModel):
    email: EmailStr
    selected_products: List


class OtpaccountaccessValidator(BaseModel):
    requested_email: EmailStr
    requested_sp_app_id: int

class VerifyProductsValidator(BaseModel):
    email: EmailStr
    selected_products: List
    otp:str


class VerifyAccountAccessValidator(BaseModel):
    requested_email: str
    requested_sp_app_id: int
    otp: str
    requested_user_id: Union[int, str, None] = None

class EmailValidator(BaseModel):
    email: EmailStr


class SubmitAccountAccessValidator(BaseModel):
    sp_apps_ids: List[int]

    @validator('sp_apps_ids')
    def check_sp_apps_ids(cls, sp_apps_ids):
        if not all(isinstance(item, int) for item in sp_apps_ids):
            raise ValueError('sp_apps_ids must be a list of integers')
        return sp_apps_ids


class ApproveRejectAccountAccessValidator(BaseModel):
    email: EmailStr
    accepted_sp_apps_ids: List[int]=[]
    rejected_sp_apps_ids: List[int]=[]
    
    @validator('accepted_sp_apps_ids')
    def check_sp_apps_ids(cls, accepted_sp_apps_ids):
        if not all(isinstance(item, int) for item in accepted_sp_apps_ids):
            raise ValueError('accepted_sp_apps_ids must be a list of integers')
        return accepted_sp_apps_ids
    
    @validator('rejected_sp_apps_ids')
    def check_rejected_sp_apps_ids(cls, rejected_sp_apps_ids):
        if not all(isinstance(item, int) for item in rejected_sp_apps_ids):
            raise ValueError('rejected_sp_apps_ids must be a list of integers')
        return rejected_sp_apps_ids


class SPApp(BaseModel):
    requested_email: str
    requested_user_id: str
    requested_date: datetime
    sp_app_name: str
    sp_app_id: int

class User(BaseModel):
    id: int
    username: str
    email: str
    sp_apps: List[SPApp]

class UsersList(BaseModel):
    users_list: List[User]

class ContactNoValidatorOut(BaseModel):
    contact_no: str
    cookie_verification: bool

class ContactNoValidator(BaseModel):
    email: EmailStr
    contact_no: str

    @validator("contact_no")
    def contact_no_validator(cls, value):
        # regex = '^[+][0-9]{2}[0-9]{3}[0-9]{7}$'
        regex = '^[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}$'
        if not re.search(regex, value):
            raise ValueError("invalid format")
        return value


class OtpSmsValidator(BaseModel):
    otp_sms: str
    contact_no: str
    email:EmailStr

    @validator("otp_sms")
    def otp_sms_validator(cls, value):
        if len(value) != 4:
            raise ValueError("OTP length should be 4 digits ")
        return value


    @validator("contact_no")
    def contact_no_validator(cls, value):
        # regex = '^[+][0-9]{2}[0-9]{3}[0-9]{7}$'
        regex = '^[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}$'
        if not re.search(regex, value):
            raise ValueError("invalid format")
        return value


class SPApp(BaseModel):
    requested_email: str
    requested_user_id: Union[str,int]=None
    sp_app_name: str
    sp_apps_logo:str
    sp_app_id: int
    is_accessible:bool
    status:str=None

class User(BaseModel):
    id: int
    username: str
    email: str
    requested_date: datetime
    sp_apps: List[SPApp]



class GetAccountAccessRequestUsersListValidatorOut(BaseModel):
    metadata: MetaDataValidator = Field(alias="_metadata")
    users_data: Optional[List[User]]=None
    message: str
    status_code: int