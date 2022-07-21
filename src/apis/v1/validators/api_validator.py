from pydantic_sqlalchemy import sqlalchemy_to_pydantic
from pydantic import typing
from src.apis.v1.models.api_model import api
from src.apis.v1.validators.action_validator import ActionValidator

ApiValidator = sqlalchemy_to_pydantic(api)

class ApiWithActionsValidator(ApiValidator):
    action: typing.List[ActionValidator] = []