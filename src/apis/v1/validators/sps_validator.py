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
