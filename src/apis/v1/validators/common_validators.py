from pydantic import BaseModel


class SuccessfulResponseValidator(BaseModel):
    message: str
    status: bool = True


class ErrorResponseValidator(BaseModel):
    message: str
    status: bool = False


class SuccessfulJsonResponseValidator(BaseModel):
    message: str
    statuscode: int


class GeneralBaseModelErrors(BaseModel):
    detail = [
        {
            "loc": [
                "body",
                "audit_log_access_level"
            ],
            "msg": "unexpected value; permitted: 'read-only', 'full-access'",
            "type": "value_error.const",
            "ctx": {
                "given": "Afull-access",
                "permitted": [
                    "read-only",
                    "full-access"
                ]
            }
        }
    ]
