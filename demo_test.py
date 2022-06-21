import json
import unittest
from src.apis.v1.controllers.sps_controller import SPSController
import load_env
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.apis.v1.models import *
from src.apis.v1.core.project_settings import Settings


SQLALCHEMY_DATABASE_URL = Settings().DATABASE_URL
engine = create_engine(SQLALCHEMY_DATABASE_URL)
session_ = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = session_()
current_user_email = "umair@gmail.com"
resp = SPSController(db).get_sps(current_user_email)
# data = json.vars(resp)
# print(data)
print(vars(resp))