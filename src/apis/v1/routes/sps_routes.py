from fastapi import APIRouter, Depends
from src.apis.v1.controllers.sps_controller import SPSController

from src.apis.v1.validators.sps_validator import ListServiceProviderValidatorOut, ServiceProviderValidator
from src.apis.v1.validators.common_validators import ErrorResponseValidator
from src.apis.v1.db.session import engine, get_db
from sqlalchemy.orm import Session
from fastapi_jwt_auth import AuthJWT
from . import oauth2_scheme

router = APIRouter(tags=["Service Providers"])


@router.get("/service-providers", summary="Get All Service Providers Api",
            responses={200:{"model":ListServiceProviderValidatorOut,"description":"Succesfully returned service providers"},
            500:{"description":"Internal Server Error","model":ErrorResponseValidator},
            404:{"description":"No service providers found against this email","model":ErrorResponseValidator}})
async def list_service_providers(authorize: AuthJWT = Depends(),token: str = Depends(oauth2_scheme),db: Session = Depends(get_db),):
    '''
     List All Service Providers
    '''
    authorize.jwt_required()

    current_user_email = authorize.get_jwt_subject()
    resp = SPSController(db).get_sps(current_user_email)
    return resp

@router.get("/service-providers/{serviceprovider}", summary="Get Specific Service Providers Api")
async def read_user(serviceprovider: str,authorize: AuthJWT = Depends(),token: str = Depends(oauth2_scheme)):
    authorize.jwt_required()
    return {"service_provider": serviceprovider}

@router.post("/service-provider", summary="Create Service Provider Api")
async def create_service_provider(serviceprovidervalidator: ServiceProviderValidator,serviceprovider: str,authorize: AuthJWT = Depends(),token: str = Depends(oauth2_scheme),db: Session = Depends(get_db)):
    authorize.jwt_required()
    resp = SPSController(db).create_sps(**serviceprovidervalidator.dict())
    return resp
    # return {"service_provider": serviceprovider}