from src.apis.v1.models.samlusersessionmodel import SAMLUserSession


class FrontendSessionService():
    def __init__(self, db):
        self.db = db

    def insert_frontend_session_saml(self, **kwargs):
        try:
            print('stored frontend session-------------------')
            add_session = SAMLUserSession(**kwargs)
            self.db.add(add_session)
            self.db.commit()
            return "created idp user", 200
        except Exception as e:
            return "Error: {}".format(e), 500

    def get_frontend_session_saml(self, cookie_id):
        try:
            return self.db.query(SAMLUserSession).filter_by(cookie_id=cookie_id).first()
        except:
            return None

    def delete_session(self, cookie_id):
        try:
            user_delete = self.get_frontend_session_saml(cookie_id)
            self.db.delete(user_delete)
            self.db.commit()
            return "deleted user session"
        except Exception as e:
            return "Error: {}".format(e), 500