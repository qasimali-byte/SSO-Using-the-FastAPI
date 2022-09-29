from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from typing import Generator
from src import Base

# For postgres database
SQLALCHEMY_DATABASE_URL = "postgresql://asad:postgres@localhost:5432/ssoidp"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

def override_get_db() -> Generator:
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()