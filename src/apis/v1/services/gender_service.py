from src.apis.v1.models.gender_model import gender
from src.apis.v1.validators.gender_validator import GenderValidator


class GenderService():
    def __init__(self, db) -> None:
        self.db = db

    def get_genders_db(self):
        gender_object = self.db.query(gender).all()
        gender_data = GenderValidator(gender=gender_object).dict()
        return gender_data
        