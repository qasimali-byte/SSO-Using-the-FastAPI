from fastapi import APIRouter, Depends
from src.apis.v1.controllers.sps_controller import SPSController
from src.apis.v1.helpers.role_verifier import RoleVerifierImplemented

from src.apis.v1.validators.sps_validator import ListServiceProviderValidatorOut, ServiceProviderValidator
from src.apis.v1.validators.common_validators import ErrorResponseValidator
from src.apis.v1.db.session import engine, get_db
from sqlalchemy.orm import Session
from . import oauth2_scheme

router = APIRouter(tags=["Service Providers"])


@router.get("/service-providers", summary="Get All Service Providers Api",
            responses={200:{"model":ListServiceProviderValidatorOut,"description":"Succesfully returned service providers"},
            500:{"description":"Internal Server Error","model":ErrorResponseValidator},
            404:{"description":"No service providers found against this email","model":ErrorResponseValidator}})
async def list_service_providers(user_email_role:RoleVerifierImplemented = Depends(),token: str = Depends(oauth2_scheme),db: Session = Depends(get_db),):
    '''
     List All Services Providers
    '''
    current_user_email = user_email_role.get_user_email()
    resp = SPSController(db).get_sps(current_user_email)
    return resp

@router.get("/service-providers/{serviceprovider}", summary="Get Specific Service Providers Api")
async def read_user(serviceprovider: str,user_email_role:RoleVerifierImplemented = Depends(),token: str = Depends(oauth2_scheme)):

    return {"service_provider": serviceprovider}

@router.post("/service-provider", summary="Create Service Provider Api")
async def create_service_provider(serviceprovidervalidator: ServiceProviderValidator,serviceprovider: str,user_email_role:RoleVerifierImplemented = Depends(),token: str = Depends(oauth2_scheme),db: Session = Depends(get_db)):

    resp = SPSController(db).create_sps(**serviceprovidervalidator.dict())
    return resp
    # return {"service_provider": serviceprovider}