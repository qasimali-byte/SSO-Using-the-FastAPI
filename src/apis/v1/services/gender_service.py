from src.apis.v1.models.gender_model import gender
from src.apis.v1.models.idp_users_model import idp_users
from src.apis.v1.utils.gender_utils import format_gender_selected_data, format_gender_selected_data_loged_in_area
from src.apis.v1.validators.gender_validator import GenderValidator
from sqlalchemy.orm import Load

class GenderService():
    def __init__(self, db) -> None:
        self.db = db

    def get_genders_db(self):
        gender_object = self.db.query(gender).all()
        gender_data = GenderValidator(gender=gender_object).dict()
        return gender_data
        
    def get_driq_selected_gender(self, selected_user_id):
        all_genders = self.get_genders_db()['gender']
        selected_gender = self.db.query(idp_users) \
        .options(Load(idp_users).load_only("id","dr_iq_gender_id")).join(gender).filter(idp_users.id == selected_user_id).scalar()
        all_genders = format_gender_selected_data(all_genders,selected_gender)
        return all_genders

    def get_driq_selected_gender_loged_in_user(self, selected_user_id):
        selected_gender = self.db.query(idp_users) \
        .options(Load(idp_users).load_only("id","dr_iq_gender_id")).join(gender).filter(idp_users.id == selected_user_id).scalar()
        all_genders = format_gender_selected_data_loged_in_area(selected_gender)
        return all_genders