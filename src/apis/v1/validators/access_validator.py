from typing import Union
from pydantic import BaseModel,EmailStr, validator
from pydantic.class_validators import List
import re

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
    email: EmailStr
    product: str

class VerifyProductsValidator(BaseModel):
    email: EmailStr
    selected_products: List
    otp:str


class VerifyAccountAccessValidator(BaseModel):
    email: EmailStr
    requested_product: str
    otp: str
    is_verified: bool
    requested_email: str
    requested_user_id: Union[int, str, None] = None

class EmailValidator(BaseModel):
    email: EmailStr


class SubmitAccountAccessValidator(BaseModel):
    email: EmailStr
    sp_apps_ids: List[int]

    @validator('sp_apps_ids')
    def check_sp_apps_ids(cls, sp_apps_ids):
        if not all(isinstance(item, int) for item in sp_apps_ids):
            raise ValueError('sp_apps_ids must be a list of integers')
        return sp_apps_ids




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
