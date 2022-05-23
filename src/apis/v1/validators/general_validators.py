from pydantic import BaseModel
class SuccessfulResponseValidator(BaseModel):
    message: str
    status: bool = True

class ErrorResponseValidator(BaseModel):
    message: str
    status: bool = False