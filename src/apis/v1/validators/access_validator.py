from pydantic import BaseModel,EmailStr
from pydantic.class_validators import List


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
