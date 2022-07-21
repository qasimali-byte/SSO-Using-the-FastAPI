from datetime import datetime
from src.apis.v1.helpers.custom_exceptions import CustomException
from src.apis.v1.models.api_model import api
from sqlalchemy.orm import subqueryload
from src.apis.v1.models.user_action_model import user_action
from src.apis.v1.validators.api_validator import ApiValidator, ApiWithActionsValidator


class ActionService:
    def __init__(self, db) -> None:
        self.db = db

    def get_action_api(self, method, url):
        api_data = self.db.query(api).options(subqueryload(api.action)).filter(api.method == method, api.name == url).first()
        if not api_data:
            return None
        api_with_actions = ApiWithActionsValidator.from_orm(api_data)
        return api_with_actions.dict()

    def store_user_action_logs(self, action_list: list, status: str, user_id:str, role_name:str, app_name: str = None):
        try:
            list_user_action_data = []
            for action in action_list:
                list_user_action_data.append(user_action(idp_user_id=user_id, action_id=action["id"], role_name=role_name, 
                app_name=app_name,status=status, action_date=datetime.now()))

            self.db.bulk_save_objects(list_user_action_data)
            self.db.commit()
            return

        except Exception as e:
            raise CustomException(message= str(e) + self.error_string +"- error occured in Action Service", status_code= status.HTTP_500_INTERNAL_SERVER_ERROR)