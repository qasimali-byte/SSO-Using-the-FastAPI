from pydantic import BaseModel, validator
from typing import List,Dict, Optional

class ServiceProviderValidator(BaseModel):
    name : str
    info : str
    host : str
    sp_metadata : str

class ListServiceProviders(BaseModel):
    id: int
    name : str
    image : str
    host_url : str
    is_accessible : bool
    
class ListServiceProviderValidatorOut(BaseModel):
    serviceproviders: Optional[List['ListServiceProviders']] = None
    message : str = "success"
    statuscode : int = 200

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