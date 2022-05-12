import load_env
from src.apis.v1.core.project_settings import Settings
settings_by_env = Settings()
from src.config.constants import Constants
from src.apis.v1.db.session import engine
from src.apis.v1.models import Base
def create_tables():
    Base.metadata.create_all(bind=engine)
create_tables()

from src.apis.v1.helpers.super_admin import create_super_admin
from src.apis.v1.db.session import SessionLocal
db = SessionLocal()
create_super_admin(db)