from src.apis.v1.models.idp_user_types_model import idp_user_types
from src.apis.v1.validators.type_of_user_validator import TypeOfUserValidator


class TypeOfUserService:
    def __init__(self, db):
        self.db = db

    def get_type_of_user_db(self, type_of_user):
        try:
            type_of_user_object = self.db.query(idp_user_types).filter(idp_user_types.user_type == type_of_user).first()
            return TypeOfUserValidator.from_orm(type_of_user_object).dict()
        except Exception as e:
            return None