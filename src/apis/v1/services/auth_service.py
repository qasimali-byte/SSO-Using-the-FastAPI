from src.apis.v1.models.idp_users_model import idp_users
from src.apis.v1.utils.auth_utils import verify_password
from sqlalchemy import and_
class AuthService:

    def __init__(self, db):
        self.db = db

    def get_idp_user(self, email: str):
        user=self.db.query(idp_users).filter(and_(idp_users.email==email,idp_users.is_approved==True,idp_users.is_active==True)).first()
        return user

    def check_email_initial(self, email:str):
        user=self.db.query(idp_users).filter(and_(idp_users.email==email)).first()
        return user

    def check_email(self, email: str):
        if self.get_idp_user(email):
            return True
        else:
            return False

    def insert_idp_user(self, **kwargs):
        try:
            create_user = idp_users(**kwargs)
            self.db.add(create_user)
            self.db.commit()
            return "created idp user", 200
        except Exception as e:
            return "Error: {}".format(e), 500

    def authenticate_user(self, email: str, password: str):
        user = self.get_idp_user(email)
        if not user:
            return False
        if not verify_password(password, user.password_hash):
            return False
        return user