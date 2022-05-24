from pydantic import BaseModel, validator

class ServiceProviderValidator(BaseModel):
    name : str
    info : str
    host : str
    sp_metadata : str