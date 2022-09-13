from src.apis.v1.services.practices_service import PracticesService


class PracticesController:
    def __init__(self, db):
        self.db = db

    def assign_practices_to_user(self, **kwargs):
        return PracticesService(self.db).assign_practices_user_db(**kwargs)

    def get_allowed_practices_by_userid(self, app_id, user_id, selected_id):

        practices_object = PracticesService(self.db)
        total_practices_allowed = practices_object.get_selected_practices_db_by_id(app_id,user_id, selected_id)
        return total_practices_allowed
    
    def get_allowed_practices_by_userid_loged_in_user(self, app_id, user_id, selected_id):

        practices_object = PracticesService(self.db)
        total_practices_allowed = practices_object.get_selected_practices_db_by_id_loged_in_user(app_id,user_id, selected_id)
        return total_practices_allowed
    