from pydantic import BaseModel, validator, typing

class SPPracticesValidator(BaseModel):
    id: int
    name: str
class ListSPRegionsValidator(BaseModel):
    id: int
    name: str
    practices: typing.List[SPPracticesValidator]

class SPRegionsValidator(BaseModel):
    """
        List SP Practices Validator
    """
    __root__: typing.List[ListSPRegionsValidator]