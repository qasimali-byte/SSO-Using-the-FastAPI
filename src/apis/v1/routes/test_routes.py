from fastapi import APIRouter, Request

from src.apis.v1.validators.auth_validators import EmailValidator

router = APIRouter(tags=["test"])

@router.post("/test1", summary="Find User Email in Product 1")
def user_email_product1(email_validator: EmailValidator):
    return {'email':'user email found in product 1'}


@router.post("/test2", summary="Find User Email in Product 2")
def user_email_product2(email_validator: EmailValidator):
    return {'email':'user email found in product 2'}