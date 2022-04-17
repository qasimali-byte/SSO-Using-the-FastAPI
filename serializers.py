from typing import Any
# from urllib.error import HTTPError
import uuid
from fastapi import HTTPException
from pydantic import BaseModel, validator
from sqlalchemy.dialects.postgresql import UUID
from saml2 import (
    BINDING_HTTP_POST,
    BINDING_HTTP_REDIRECT,
    entity,
    server
)

class SessionSerializer(BaseModel):
    cookie_id: uuid.UUID
    user_id: str

# x = SessionSerializer(cookie_id="f8a8705b-d09c-4a37-9ad4-6f5d7c6b2798", user_id="123")

class SamlRequestSerializer(BaseModel):
    SAMLRequest: str
        
    @validator('SAMLRequest')
    def verify_saml_request(cls, saml_request: str) -> str:
        idp_server = server.Server(config_file="./idp_conf.py")
        # idp_server.config.setattr("idp", "want_authn_requests_signed", True)
        try:
            data = idp_server.parse_authn_request(saml_request,BINDING_HTTP_REDIRECT)
        except Exception as e:
            raise HTTPException(status_code=403, detail="Invalid SAML Request")
        