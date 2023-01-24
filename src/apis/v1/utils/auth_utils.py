from passlib import pwd
from passlib.context import CryptContext
from typing import Optional
from datetime import datetime, timedelta
from jose import JWTError, jwt
from src.apis.v1.core.project_settings import Settings
from src.apis.v1.helpers.auth import AuthJWT

from saml2.saml import NAMEID_FORMAT_EMAILADDRESS, NAMEID_FORMAT_UNSPECIFIED, NameID, NAMEID_FORMAT_TRANSIENT
from saml2.time_util import in_a_while
from saml2 import (
    BINDING_HTTP_POST,
    BINDING_HTTP_REDIRECT,
    entity,
    BINDING_SOAP
)
import requests
from saml2.samlp import SessionIndex
from saml2 import server

from fastapi import HTTPException,status

settings = Settings()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def create_password_hash(password):
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def generate_password(size=9, custom=True):
    """
    minimum length returned is 9.
    "ascii_62" (the default) – all digits and ascii upper & lowercase letters.
    Provides ~5.95 entropy per character.
    "ascii_50" – subset which excludes visually similar characters (1IiLl0Oo5S8B).
    Provides ~5.64 entropy per character.
    "ascii_72" – all digits and ascii upper & lowercase letters, as well as some punctuation.
     Provides ~6.17 entropy per character.
    "hex" – Lower case hexadecimal. Providers 4 bits of entropy per character.
    """
    if custom:
        # confusing letters (1IiLl0OoS5) are excluded.
        characters = "abcdefghjkmnpqrtuvwxyzABCDEFGHJKMNPQRSTUVWXYZ2346789!@#-$%&?;*"
        return pwd.genword(length=size, entropy=52, chars=characters)
    else:
        return pwd.genword(length=size, entropy=52, charset="ascii_72")

# async def get_current_user(token: str = Depends(oauth2_scheme)):
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )
#     try:
#         payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
#         username: str = payload.get("sub")
#         if username is None:
#             raise credentials_exception
#         token_data = TokenData(username=username)
#     except JWTError:
#         raise credentials_exception
#     user = get_user(fake_users_db, username=token_data.username)
#     if user is None:
#         raise credentials_exception
#     return user
#print('just added comment')
def get_current_logged_in_user(authorize, response_body):
    current_user = None
    try:
         current_user = authorize.get_jwt_subject()
    except:
        current_user = None

    if current_user == None:
        access_token = response_body.get("access_token",None)
        if access_token:
            current_user = authorize._verified_token(access_token)['sub']

    return current_user




def auth_jwt_verifier_and_get_subject(request):
    authorize=AuthJWT(request)
    current_user_email = authorize.get_jwt_subject()
    return current_user_email

def logout_request_from_idp(sp_entity_id,destination_url, name_id):
        
    idp_server = server.Server(config_file="idp/idp_conf.py")
    nid = NameID(name_qualifier="foo", format=NAMEID_FORMAT_TRANSIENT,
                 text=name_id)

    req_id, req = idp_server.create_logout_request(
        issuer_entity_id=sp_entity_id,
        destination=destination_url,
        name_id=nid, reason="Tired", expire=in_a_while(minutes=15),
        session_indexes=["_foo"])

    info = idp_server.apply_binding(
        BINDING_SOAP, req, destination_url,
        relay_state="relay2")
    redirect_url = None
    print('sp_entity_id','-----',sp_entity_id,'destination_url','-----------',destination_url,'---',name_id)
    try:
        response = requests.post(info['url'], data=info['data'], headers={'Content-Type': 'application/xml'})
        return response.status_code
    except Exception as e:
        return status.HTTP_200_OK

