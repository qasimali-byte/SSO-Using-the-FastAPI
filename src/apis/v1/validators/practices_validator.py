from pydantic import BaseModel, validator, typing

class ListSPPracticesValidator(BaseModel):
    id: int
    name: str

class SPPracticesValidator(BaseModel):
    """
        List SP Practices Validator
    """
    __root__: typing.List[ListSPPracticesValidator]