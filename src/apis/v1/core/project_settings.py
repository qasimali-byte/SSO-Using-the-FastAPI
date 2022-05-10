import os
from pathlib import Path
from dotenv import load_dotenv
from pydantic import BaseSettings
class Settings(BaseSettings):
    PROJECT_TITLE: str = "SSO IDP"
    PROJECT_VERSION: str = "0.0.1"
    HOST_URL: str = os.environ.get("HOST_URL")
    HOST_PORT: int = int(os.environ.get("HOST_PORT"))
    POSTGRES_USER: str = os.environ.get("POSTGRES_USER",)
    POSTGRES_PASSWORD: str = os.environ.get("POSTGRES_PASSWORD")
    POSTGRES_SERVER: str = os.environ.get("POSTGRES_SERVER")
    POSTGRES_PORT: int = int(os.environ.get("POSTGRES_PORT", 5432))
    POSTGRES_DB: str = os.environ.get("POSTGRES_DB")
    DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"

def settings():
    return Settings()
