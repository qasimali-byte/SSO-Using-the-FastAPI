from src.apis.v1.core.project_settings import Settings
settings_by_env = Settings()
from src.config.constants import Constants
from src.apis.v1.db.session import engine
from src.apis.v1.models import Base
import os, sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)))
def create_tables():
    Base.metadata.create_all(bind=engine)
create_tables()