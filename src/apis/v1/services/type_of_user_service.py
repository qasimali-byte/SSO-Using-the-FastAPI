from src.apis.v1.models.idp_user_types_model import idp_user_types


class TypeOfUserService():
    def __init__(self, db):
        self.db = db

    def get_type_of_user_db(self, type_of_user):
        try:
            return self.db.query(idp_user_types).filter(idp_user_types.user_type == type_of_user).first()
        except Exception as e:
            print(e)
            return None