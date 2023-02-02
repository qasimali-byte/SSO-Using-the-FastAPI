from fastapi import Depends, APIRouter, Request
from starlette import status
from src.apis.v1.validators.common_validators import SuccessfulResponseValidator
from src.apis.v1.db.session import get_db
from sqlalchemy.orm import Session
from src.apis.v1.helpers.role_verifier import RoleVerifierImplemented
from . import oauth2_scheme
from src.apis.v1.validators.common_validators import ErrorResponseValidator, SuccessfulJsonResponseValidator
from ..controllers.access_controller import AccessController
from ..helpers.auth import AuthJWT
from ..helpers.customize_response import custom_response
from ..services.access_service import AccessService
from ..validators.access_validator import OtpSmsValidator, ContactNoValidator, ContactNoValidatorOut, EmailValidator, OtpEmailValidator, OtpProductsValidator, \
    VerifyProductsValidator, OtpAccountValidator
from celery_worker import otp_sender
from sqlalchemy.ext.asyncio import AsyncSession
from src.graphql.db.session import get_session_without_context_manager
from src.packages.two_factor_authentication.cookie_two_factor_authentication import create_phone_cookie

router = APIRouter(tags=["Account Access"])


@router.post("/request-account", summary=" Load all the registered apps and emails in SSO.",
             responses={200: {"model": SuccessfulJsonResponseValidator}}, status_code=200)
async def request_account(user_email_role:RoleVerifierImplemented = Depends(),db: Session = Depends(get_db),authorize: AuthJWT = Depends(), token: str = Depends(oauth2_scheme)):

    """
        This api returns the emails and apps list to grant access using emails.

    """

    current_user_email = user_email_role.get_user_email()
    user_data = AccessService(db).get_user_apps_info_db(user_email=current_user_email)
    user_data["user"] = dict({"name": user_data.get("user").first_name,
                              "id": user_data.get("user").id,
                              "is_active": user_data.get("user").is_active})
    return user_data


@router.post("/send-otp", summary="Send OTP via email",
             responses={200: {"model": SuccessfulJsonResponseValidator},
                        400: {"model": ErrorResponseValidator},
                        500:{"description":"Internal Server Error","model":ErrorResponseValidator 
                        }})
async def send_otp(email_validator: OtpEmailValidator, db: Session = Depends(
    get_db)): # ,authorize: AuthJWT = Depends(), token: str = Depends(oauth2_scheme)):

    """
        This api returns the emails and apps list to grant access using emails.
        after receiving email, verify whether its register.
    """
    response = AccessController(db).send_otp_email(email=email_validator.email, product_name=email_validator.product_name,product_id=email_validator.product_id)
    return response



@router.post("/send-email-super-admin", summary="Send Phone Number Changed email to Super Admin",
             responses={200: {"model": SuccessfulJsonResponseValidator}}, status_code=200)
async def send_email_super_admin(contact_validator: ContactNoValidator, db: Session = Depends(
    get_db)): # ,authorize: AuthJWT = Depends(), token: str = Depends(oauth2_scheme)):

    response = AccessController(db).send_email_to_super_admin(contact_validator.email, contact_validator.contact_no)
    return response





@router.post("/verify-otp", summary="Verify OTP", responses={200: {"model": SuccessfulJsonResponseValidator}}, status_code=200)
async def request_account(otp_validator: OtpAccountValidator, db: Session = Depends(get_db)):
    """
        This api verifies emails using OTPs sent previously.
    """

    response = AccessController(db).verify_otp_email(otp_validator=otp_validator)
    return response


@router.post("/send-otp-products", summary="Send OTP via email",
             responses={200: {"model": SuccessfulJsonResponseValidator}}, status_code=200)
async def send_otp_products(products_validator: OtpProductsValidator,
                            db: Session = Depends(get_db),
                            async_db: AsyncSession = Depends(get_session_without_context_manager)
                            ):
    """
        This api returns the apps list to create user for those apps.

    """
    response = await AccessController(db).send_otp_products_email(products_validator,async_db=async_db)
    return response


@router.post("/verify-otp-products", summary="Verify OTP")
async def verify_otp_products(otp_products_validator: VerifyProductsValidator,
                              # authorize: AuthJWT = Depends(),
                              # token: str = Depends(oauth2_scheme),
                              # user_email_role:RoleVerifierImplemented = Depends(),
                              db: Session = Depends(get_db)):
    """
        This api verifies emails using OTPs sent previously.
    """
    response = AccessController(db).verify_otp_products_email(otp_products_validator)
    return response


@router.post("/get_contact_no_by_email", summary="Get contact_no for an email if exists",
             responses={200: {"model": ContactNoValidatorOut}, 404: {"model": ErrorResponseValidator, "description" : "Error occurred when not found"}})
async def get_contact_no_by_email(user_email: EmailValidator, request: Request, db: Session = Depends(get_db)):
    """
         This apis checks if a number exists in db against an email
    """
    response = AccessController(db).get_contact_no_by_email(user_email.email, request)

    return response


@router.post("/send-otp-sms", summary="Send OTP via SMS",
             responses={200: {"model": SuccessfulJsonResponseValidator}, 404: {"model": ErrorResponseValidator, "description" : "Error occurred when email not found"}})
async def send_otp_sms(contact_no_validator: ContactNoValidator, db: Session = Depends(get_db)):

    """
        This api sends OTP via SMS for 2FA.
    """
    response = AccessController(db).send_otp_sms(contact_no_validator.email, contact_no_validator.contact_no)
    return response


@router.post("/verify-otp-sms", summary="Verify OTP SMS", responses={200: {"model": SuccessfulJsonResponseValidator}, 406: {"model": ErrorResponseValidator, "description": "OTP verification failed"}})
async def verify_otp_sms(otp_sms_validator: OtpSmsValidator, db: Session = Depends(get_db)):
    """
        This api verifies emails using OTPs sent previously.
    """
    response = AccessController(db).verify_otp_sms(otp_sms_validator.email,otp_sms_validator.otp_sms, otp_sms_validator.contact_no)

    if response.status_code == 200:  # let's create phone cookie
        response = create_phone_cookie(response, otp_sms_validator.contact_no, db)

    return response
