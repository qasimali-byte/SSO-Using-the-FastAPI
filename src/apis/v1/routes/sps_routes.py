from fastapi import APIRouter, Depends
from src.apis.v1.controllers.sps_controller import SPSController

from src.apis.v1.validators.sps_validator import ServiceProviderValidator
from src.apis.v1.db.session import engine, get_db
from sqlalchemy.orm import Session

router = APIRouter(tags=["Service Providers"])


@router.get("/service-providers", summary="Get Service Providers Api")
async def list_service_providers(db: Session = Depends(get_db)):
    resp = SPSController(db).get_sps(useremail="")

@router.get("/service-providers/{serviceprovider}", summary="Get Service Providers Api")
async def read_user(serviceprovider: str):
    return {"service_provider": serviceprovider}

@router.post("/service-provider", summary="Create Service Provider Api")
async def create_service_provider(serviceprovidervalidator: ServiceProviderValidator,db: Session = Depends(get_db)):
    resp = SPSController(db).create_sps(**serviceprovidervalidator.dict())
    return resp
    # return {"service_provider": serviceprovider}