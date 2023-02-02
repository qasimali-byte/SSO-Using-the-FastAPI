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


class VerifyProductsValidator(BaseModel):
    email: EmailStr
    selected_products: List
    otp:str


class EmailValidator(BaseModel):
    email: EmailStr


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
