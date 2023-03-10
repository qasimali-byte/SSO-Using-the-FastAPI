from fastapi import Depends, APIRouter, Query, Request, Response
from starlette import status
from src.apis.v1.services.user_service import UserService
from src.apis.v1.validators.common_validators import SuccessfulResponseValidator
from src.apis.v1.db.session import get_db
from sqlalchemy.orm import Session
from src.apis.v1.helpers.role_verifier import RoleVerifierImplemented
from src.apis.v1.validators.sps_validator import ListUnAccessibleServiceProviderValidatorOut
from . import oauth2_scheme
from src.apis.v1.validators.common_validators import ErrorResponseValidator, SuccessfulJsonResponseValidator
from ..controllers.access_controller import AccessController
from ..helpers.auth import AuthJWT
from ..helpers.customize_response import custom_response
from ..services.access_service import AccessService
from ..validators.access_validator import ApproveAccountAccessValidator, GetAccountAccessRequestUsersListValidatorOut, OtpSmsValidator, ContactNoValidator, ContactNoValidatorOut, EmailValidator, OtpEmailValidator, OtpProductsValidator, OtpaccountaccessValidator, SubmitAccountAccessValidator, \
    VerifyProductsValidator, OtpAccountValidator,VerifyAccountAccessValidator
from celery_worker import otp_sender
from sqlalchemy.ext.asyncio import AsyncSession
from src.graphql.db.session import get_session_without_context_manager
from src.packages.two_factor_authentication.cookie_two_factor_authentication import create_phone_cookie

router = APIRouter(tags=["Account Access"])


@router.get("/request-spapps-account", summary=" Load all the registered apps and emails in SSO.",
             responses={200: {"model": ListUnAccessibleServiceProviderValidatorOut},
                        400: {"description": "Bad Request", "model": ErrorResponseValidator},
                        401: {"description": "Unauthorized", "model": ErrorResponseValidator},
                        500: {"description": "Internal Server Error", "model": ErrorResponseValidator}
            },status_code=200)
async def request_account(db: Session = Depends(get_db),authorize: AuthJWT = Depends(), token: str = Depends(oauth2_scheme)):

    """
        This api returns  apps list to on which user don't have access.
        Select query will be use over the idp_user table id_sp and spapps table 
        in id_sp table we added more fields 
        
    """
    current__user_email = authorize.get_jwt_current_user()
    user_data=AccessController(db).get_user_apps_info_db(current__user_email)
    return user_data


@router.post("/verify-account-request", summary=" This will verify the Account request.",
             responses={
                 200: {"model": SuccessfulJsonResponseValidator},
                 400: {"description": "Bad Request", "model": ErrorResponseValidator},
                 401: {"description": "Unauthorized", "model": ErrorResponseValidator},
                 500: {"description": "Internal Server Error", "model": ErrorResponseValidator}
             }, status_code=200)

async def verify_account_request(account_access_verify_validator: VerifyAccountAccessValidator,db: Session = Depends(get_db),authorize: AuthJWT = Depends(), token: str = Depends(oauth2_scheme),\
    ):

    # current_user_email = user_email_role.get_user_email()
    current__user_email = authorize.get_jwt_current_user()
    user_data=AccessController(db).verify_account_access_otp(current__user_email,account_access_verify_validator)
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


@router.post("/send-account-access-otp", summary="Send OTP via email for account access request",
             responses={200: {"model": SuccessfulJsonResponseValidator}}, status_code=200)
async def send_account_access_otp(account_access_validator: OtpaccountaccessValidator,
                            db: Session = Depends(get_db),authorize: AuthJWT = Depends(), token: str = Depends(oauth2_scheme),\
                            ):
    """
    here we call the conserned service provider API for user verification
    """
    
    response = await AccessController(db).send_otp_for_account_access_request(account_access_validator)
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



@router.put("/submit-account-access-request")
async def submit_account_access_request(submit_account_access_validator: SubmitAccountAccessValidator, db: Session = Depends(get_db),authorize: AuthJWT = Depends(), token: str = Depends(oauth2_scheme),):
    current__user_email = authorize.get_jwt_current_user()
    response=AccessController(db).submit_account_access_requests(current__user_email,submit_account_access_validator)
    return response    




@router.get(
    "/get-users-sp-apps-account-access-requests",
    summary="Load all the requested sp apps and primary emails.",
    responses={200:{"model":GetAccountAccessRequestUsersListValidatorOut},
        400: {"description": "Bad Request", "model": ErrorResponseValidator},
        401: {"description": "Unauthorized", "model": ErrorResponseValidator},
        500: {"description": "Internal Server Error", "model": ErrorResponseValidator},
    }
)
async def get_user_sp_apps_account_access_request(
    user_email_role: RoleVerifierImplemented = Depends(),
    db: Session = Depends(get_db),
    authorize: AuthJWT = Depends(),
    token: str = Depends(oauth2_scheme),
    page: int = Query(1, ge=1),
    limit: int = Query(10, le=100),
    search: str = Query(None),
):

    try:
        response=AccessController(db).get_user_sp_apps_account_access_requests(page=page, limit=limit, search=search)
        return Response(content=response, status_code=status.HTTP_200_OK)
    except Exception as e:
        return Response(content={"message": "Internal server error"}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)




@router.put("/approve-account-access-request",responses={
    200: {"description": "Account access requests submitted successfully"},
    400: {"description": "Invalid input data"},
    500: {"description": "Internal server error"},})
async def approve_account_access_request(approve_account_access_validator: ApproveAccountAccessValidator, db: Session = Depends(get_db)):
    
    try:
        response=AccessController(db).approve_account_access_requests(approve_account_access_validator)
        return response
    except Exception as e:
        return Response(content={"message": "Internal server error"}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)



