from pydantic import BaseModel, validator
from typing import List,Dict, Optional

from src.apis.v1.models.sp_apps_model import SPAPPS
from pydantic_sqlalchemy import sqlalchemy_to_pydantic

SpAppsGeneralValidator = sqlalchemy_to_pydantic(SPAPPS)

class ListSpAppsGeneralValidator(BaseModel):
    __root__: List[SpAppsGeneralValidator]
    class Config:
        orm_mode = True   
class ServiceProviderValidator(BaseModel):
    name : str
    info : str
    host : str
    sp_metadata : str

class ListServiceProviders(BaseModel):
    id: int
    display_name: str
    name : str
    image : str
    host_url : str
    is_accessible : bool
    
class ListServiceProviderValidatorOut(BaseModel):
    serviceproviders: Optional[List['ListServiceProviders']] = None
    message : str = "success"
    statuscode : int = 200



class UnAccessibleServiceProvider(BaseModel):
    app_id: int
    app_name: str
    display_name: str
    image: str
    is_verified: bool
    is_accessible: bool
    requested_email: Optional[str] = None
    is_requested:bool

class ListUnAccessibleServiceProviderValidatorOut(BaseModel):
    serviceproviders: Optional[List[UnAccessibleServiceProvider]] = None
    message: str = "success"
    statuscode: int = 200


class FilterServiceProviderValidator(BaseModel):
    
    name: str
    display_name : str
    info: str
    host : str
    logo_url : str
    sp_metadata: str
    is_active : bool

    class Config:
        orm_mode = True

class ListFilterServiceProviderValidator(BaseModel):
    __root__: List[FilterServiceProviderValidator]

    class Config:
        orm_mode = True