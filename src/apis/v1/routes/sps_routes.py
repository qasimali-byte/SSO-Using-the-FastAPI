from fastapi import APIRouter

router = APIRouter()


@router.get("/service-providers", tags=["service providers"])
async def list_service_providers():
    return [{"username": "Rick"}, {"username": "Morty"}]

@router.get("/service-providers/{serviceprovider}", tags=["service providers"])
async def read_user(serviceprovider: str):
    return {"service_provider": serviceprovider}