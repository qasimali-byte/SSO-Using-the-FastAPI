from src.apis.v1.services.practices_service import PracticesService


class PracticesController:
    def __init__(self, db):
        self.db = db

    def assign_practices_to_user(self, **kwargs):
        return PracticesService(self.db).assign_practices_user_db(**kwargs)