from src.apis.v1.models.idp_users_practices_model import idp_users_practices
from fastapi import status

class PracticesService():
    def __init__(self, db):
        self.db = db

    def assign_practices_user_db(self, user_id, practices_list):
        try:
            objects = []
            sps_practices = practices_list

            for practice in sps_practices:
                objects.append(idp_users_practices(
                    idp_users_id = user_id,
                    practices_id  = practice,
                ))

            self.db.bulk_save_objects(objects)
            self.db.commit()

            return "assigned practices to user", status.HTTP_200_OK
        except Exception as e:
            return str(e), status.HTTP_500_INTERNAL_SERVER_ERROR