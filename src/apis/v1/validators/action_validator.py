from pydantic_sqlalchemy import sqlalchemy_to_pydantic
from src.apis.v1.models.action_model import action
from src.apis.v1.models.user_action_model import user_action

StoreActionValidator = sqlalchemy_to_pydantic(user_action)
ActionValidator = sqlalchemy_to_pydantic(action)