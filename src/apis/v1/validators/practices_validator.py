from pydantic import BaseModel, validator, typing

class SPPracticesValidator(BaseModel):
    id: int
    name: str
    is_selected: typing.Optional[bool]
class ListSPRegionsValidator(BaseModel):
    id: int
    name: str
    is_selected: typing.Optional[bool]
    practices: typing.List[SPPracticesValidator]

class SPRegionsValidator(BaseModel):
    """
        List SP Practices Validator
    """
    __root__: typing.List[ListSPRegionsValidator]