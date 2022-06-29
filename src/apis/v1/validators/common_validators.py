from pydantic import BaseModel
class SuccessfulResponseValidator(BaseModel):
    message: str
    status: bool = True

class ErrorResponseValidator(BaseModel):
    message: str
    status: bool = False

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

class MetaDataValidator(BaseModel):
    page: int
    per_page: int 
    page_count: int
    total_records: int