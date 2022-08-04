from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from typing import Generator
from src import Base

# For postgres database
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:Mtbc1122@localhost:5432/sso_idp"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

def override_get_db() -> Generator:
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()