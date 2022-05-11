from sqlalchemy.orm import Session
from src.apis.v1.services.auth_service import AuthService
from fastapi.responses import JSONResponse

class AuthController:

    def __init__(self, db: Session):
        self.db = db

    def email_verification(self, email: str):
        if AuthService(self.db).check_email(email):
            json_compatible_item_data = jsonable_encoder({
                "message": "success",
                "verification":True, 
                "is_admin": True, 
                "email": email})
            response = JSONResponse(content=json_compatible_item_data)
            response.status_code = 200
            
        else:
            json_compatible_item_data = jsonable_encoder({
            "message": "invalid email",
            "verification":False, 
            })
            response = JSONResponse(content=json_compatible_item_data)
            response.status_code = 422
        
        return response

    def insert(self, **kwargs):
        try:
            create_user = idp_users(**kwargs)
            self.db.add(create_user)
            self.db.commit()
            return "created idp user", 200
        except Exception as e:
            return "Error: {}".format(e), 500

    