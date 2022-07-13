# from core.config import settings
# from core.config import settings
# from main import settings_by_env
from src.apis.v1.core.project_settings import Settings
settings_by_env = Settings()
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from typing import Generator

# For postgrSQL database
SQLALCHEMY_DATABASE_URL = settings_by_env.DATABASE_URL
engine = create_engine("postgresql://rzgkwrpyrytfqy:5e54fb5402d0bee5b63b6914ed99fad2ec10c1a6901f3a92bc239b5bda4f5c20@ec2-3-219-229-143.compute-1.amazonaws.com:5432/d32v36qske75hi")

# For SQlLite Database
# By default SQLite will only allow one thread to communicate.
# But in FastAPI, more than one thread can interact with the database
# Thus we need to override default parameter and thus setting check_same_thread : False
# This is required only for SQLite database

# SQLALCHEMY_DATABASE_URL = 'sqlite:///./sql_app.db'
# engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread" : False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# For dependency Injection
def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()