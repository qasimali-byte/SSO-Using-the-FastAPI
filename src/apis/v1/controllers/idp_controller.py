from src.apis.v1.helpers.customize_response import custom_response
from src.apis.v1.services.frontend_session_service import FrontendSessionService


class IDPController():

    def __init__(self,db) -> None:
        self.db = db

    def store_frontend_saml(self,cookie_id,saml_req):
        status = FrontendSessionService(self.db).insert_frontend_session_saml(cookie_id=cookie_id,saml_req=saml_req)
        print(status)
        if status != 200:
            data = {
                "message":"some error occured while storing session"
            }
            response = custom_response(data=data,status_code=500)
            return response

    def get_frontend_session_saml(self,cookie_id):
        data = FrontendSessionService(self.db).get_frontend_session_saml(cookie_id)
        if data:
            return data ,200
        return None,500

    def delete_frontend_session(self, cookie_id):
        FrontendSessionService(self.db).delete_session(cookie_id)