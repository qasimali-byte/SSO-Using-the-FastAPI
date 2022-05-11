from src.apis.v1.models.idp_users_model import idp_users


class AuthService:

    def __init__(self, db):
        self.db = db

    def get_idp_user(self, email: str):
        return self.db.query(idp_users).filter_by(email=email).first()

    def check_email(self, email: str):
        if self.get_idp_user(email):
            return True
        else:
            return False