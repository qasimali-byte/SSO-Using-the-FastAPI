from fastapi import APIRouter, Request, status
from src.apis.v1.helpers.customize_response import custom_response

from src.apis.v1.validators.auth_validators import EmailValidator

router = APIRouter(tags=["test"])

@router.post("/test1", summary="Find User Email in Product 1")
def user_email_product1(email_validator: EmailValidator):
    return custom_response(data={"code":404,"message":"invalid email"},status_code=status.HTTP_404_NOT_FOUND)


@router.post("/test2", summary="Find User Email in Product 2")
def user_email_product2(email_validator: EmailValidator):
    return custom_response(data={"code":404,"message":"invalid email"},status_code=status.HTTP_404_NOT_FOUND)

# @router.post