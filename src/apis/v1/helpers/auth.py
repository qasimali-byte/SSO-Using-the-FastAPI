from typing import Dict, Optional, Union
from fastapi import HTTPException, Request, Response
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import (
    InvalidHeaderError,
    JWTDecodeError,
)
import jwt

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