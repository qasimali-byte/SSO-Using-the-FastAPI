from src.apis.v1.models.idp_users_model import idp_users
from ..helpers.custom_exceptions import CustomException
from src.apis.v1.models.idp_user_types_model import idp_user_types
from src.apis.v1.validators.type_of_user_validator import TypeOfUserValidator
from fastapi import status
from sqlalchemy.orm import Load
class TypeOfUserService:
    def __init__(self, db):
        self.db = db

    def get_type_of_user_db(self, type_of_user):
        try:
            type_of_user_object = self.db.query(idp_user_types).filter(idp_user_types.user_type == type_of_user).first()
            return TypeOfUserValidator.from_orm(type_of_user_object).dict()
        except Exception as e:
            raise CustomException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, message=str(e)+"error occured in type of user service")

    def get_type_of_user_db_by_userid(self, user_id):
        data = self.db.query(idp_user_types).options(Load(idp_user_types).load_only('id','user_type')) \
        .join(idp_users, idp_users.user_type_id == idp_user_types.id).filter(idp_users.id == user_id).first()

        if data:
            return TypeOfUserValidator.from_orm(data).dict()
