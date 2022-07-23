from src.apis.v1.controllers.roles_controller import RolesController
from src.apis.v1.controllers.user_controller import UserController
from src.apis.v1.services.action_service import ActionService
from src.apis.v1.utils.auth_utils import get_current_logged_in_user

class ActionController():
    def __init__(self, db):
        self.db = db

    def store_logs_db(self, authorize, resp_body, method, url, status_of_api):
        action_service_obj = ActionService(self.db)
        data = action_service_obj.get_action_api(method=method,url=url)

        if data:
            app_name = resp_body.get("product_name",None)
            actions = data['action']
            current_user = get_current_logged_in_user(authorize=authorize, response_body=resp_body)
            if current_user:
                user_object = UserController(self.db).get_user_by_email(current_user)
                user_id = user_object.id
                role_name = None
                role_name = role_name if RolesController(self.db).get_ezlogin_user_role(user_id) else None
                action_service_obj.store_user_action_logs(action_list=actions, status=status_of_api, user_id=user_id, 
                app_name=app_name, role_name=role_name)
                print("stored action logs")
