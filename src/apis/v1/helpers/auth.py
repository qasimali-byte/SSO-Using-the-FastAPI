from typing import Dict, List, Optional, Union,Sequence
from fastapi import HTTPException, Request, Response
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import (
    InvalidHeaderError,
    JWTDecodeError,
)
import jwt
from datetime import datetime, timedelta, timezone


class AuthJWT(AuthJWT):
    def __init__(self, req: Request = None, res: Response = None):
        super().__init__(req, res)

    def _verified_token(self,encoded_token: str, issuer: Optional[str] = None) -> Dict[str,Union[str,int,bool]]:
        """
        Verified token and catch all error from jwt package and return decode token

        :param encoded_token: token hash
        :param issuer: expected issuer in the JWT

        :return: raw data from the hash token in the form of a dictionary
        """
        algorithms = self._decode_algorithms or [self._algorithm]

        try:
            unverified_headers = self.get_unverified_jwt_headers(encoded_token)
        except Exception as err:
            raise InvalidHeaderError(status_code=422,message=str(err))

        try:
            secret_key = self._get_secret_key(unverified_headers['alg'],"decode")
        except Exception:
            raise

        try:
            return jwt.decode(
                encoded_token,
                secret_key,
                issuer=issuer,
                audience=self._decode_audience,
                leeway=self._decode_leeway,
                algorithms=algorithms
            )
        except jwt.ExpiredSignatureError:
            raise JWTDecodeError(status_code=401,message="Token expired")
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail='Invalid token')
        except Exception as err:
            raise JWTDecodeError(status_code=422,message=str(err))
        
        



    def _create_access_token(
        self,
        subject: Union[str,int],
        type_token: str,
        exp_time: Optional[int],
        fresh: Optional[bool] = False,
        algorithm: Optional[str] = None,
        headers: Optional[Dict] = None,
        issuer: Optional[str] = None,
        audience: Optional[Union[str,Sequence[str]]] = None,
        user_claims: Optional[Dict] = {},
        roles: Optional[List] = []
    ) -> str:
        """
        Create token for access_token and refresh_token (utf-8)

        :param subject: Identifier for who this token is for example id or username from database.
        :param type_token: indicate token is access_token or refresh_token
        :param exp_time: Set the duration of the JWT
        :param fresh: Optional when token is access_token this param required
        :param algorithm: algorithm allowed to encode the token
        :param headers: valid dict for specifying additional headers in JWT header section
        :param issuer: expected issuer in the JWT
        :param audience: expected audience in the JWT
        :param user_claims: Custom claims to include in this token. This data must be dictionary

        :return: Encoded token
        """
        # Validation type data
        if not isinstance(subject, (str,int)):
            raise TypeError("subject must be a string or integer")
        if not isinstance(fresh, bool):
            raise TypeError("fresh must be a boolean")
        if audience and not isinstance(audience, (str, list, tuple, set, frozenset)):
            raise TypeError("audience must be a string or sequence")
        if algorithm and not isinstance(algorithm, str):
            raise TypeError("algorithm must be a string")
        if user_claims and not isinstance(user_claims, dict):
            raise TypeError("user_claims must be a dictionary")

        # Data section
        reserved_claims = {
            "sub": subject,
            "roles": roles,
            "iat": super()._get_int_from_datetime(datetime.now(timezone.utc)),
            "nbf": super()._get_int_from_datetime(datetime.now(timezone.utc)),
            "jti": super()._get_jwt_identifier()
        }

        custom_claims = {"type": type_token}

        # for access_token only fresh needed
        if type_token == 'access':
            custom_claims['fresh'] = fresh
        # if cookie in token location and csrf protection enabled
        if super().jwt_in_cookies and super()._cookie_csrf_protect:
            custom_claims['csrf'] = super()._get_jwt_identifier()

        if exp_time:
            reserved_claims['exp'] = exp_time
        if issuer:
            reserved_claims['iss'] = issuer
        if audience:
            reserved_claims['aud'] = audience

        algorithm = algorithm or self._algorithm

        try:
            secret_key = super()._get_secret_key(algorithm,"encode")
        except Exception:
            raise

        return jwt.encode(
            {**reserved_claims, **custom_claims, **user_claims},
            secret_key,
            algorithm=algorithm,
            headers=headers
        ).decode('utf-8')        
        
    def create_access_token(self, 
                            subject: Union[str, int], 
                            fresh: Optional[bool] = False, 
                            algorithm: Optional[str] = None, 
                            headers: Optional[Dict] = None, 
                            expires_time: Optional[Union[timedelta, int, bool]] = None, 
                            audience: Optional[Union[str, Sequence[str]]] = None,
                            roles: Optional[list] = [],
                            user_claims: Optional[Dict] = {}) -> str:
        
        return self._create_access_token(
            subject=subject,
            type_token="access",
            exp_time=super()._get_expired_time("access",expires_time),
            fresh=fresh,
            algorithm=algorithm,
            headers=headers,
            audience=audience,
            user_claims=user_claims,
            issuer=super()._encode_issuer,
            roles=roles
        )
        


    def create_refresh_token(
        self,
        subject: Union[str,int],
        algorithm: Optional[str] = None,
        headers: Optional[Dict] = None,
        expires_time: Optional[Union[timedelta,int,bool]] = None,
        audience: Optional[Union[str,Sequence[str]]] = None,
        user_claims: Optional[Dict] = {},
        roles: Optional[list] = []
    ) -> str:
        """
        Create a refresh token with 30 days for expired time (default),
        info for param and return check to function create token

        :return: hash token
        """
        return self._create_access_token(
            subject=subject,
            type_token="refresh",
            exp_time=super()._get_expired_time("refresh",expires_time),
            algorithm=algorithm,
            headers=headers,
            audience=audience,
            user_claims=user_claims,
            roles=roles
            
        )

    
    
    
    
    
    

    def get_jwt_subject(self) -> Optional[Union[str,int]]:
        """
        this will return the subject of the JWT that is accessing this endpoint.
        If no JWT is present, `None` is returned instead.

        :return: sub of JWT
        """
        super().jwt_required()
        return super().get_jwt_subject()

    def get_jwt_current_user(self):
        return super().get_jwt_subject()