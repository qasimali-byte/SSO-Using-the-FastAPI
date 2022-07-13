from datetime import timedelta
import os
from pydantic import BaseSettings
class Settings(BaseSettings):
    PROJECT_TITLE: str = "SSO IDP"
    PROJECT_VERSION: str = "0.0.1"
    HOST_HTTP: str = os.environ.get("HOST_HTTP","http://")
    HOST_URL: str = os.environ.get("HOST_URL")
    HOST_PORT: int = int(os.environ.get("HOST_PORT"))
    BASE_URL: str = HOST_HTTP+HOST_URL+":"+str(HOST_PORT)
    POSTGRES_USER: str = os.environ.get("POSTGRES_USER",)
    POSTGRES_PASSWORD: str = os.environ.get("POSTGRES_PASSWORD")
    POSTGRES_SERVER: str = os.environ.get("POSTGRES_SERVER")
    POSTGRES_PORT: int = int(os.environ.get("POSTGRES_PORT", 5432))
    POSTGRES_DB: str = os.environ.get("POSTGRES_DB")
    DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"
    authjwt_secret_key = os.environ.get("SECRET_KEY")
    authjwt_denylist_enabled: bool = True
    authjwt_denylist_token_checks: set = {"access","refresh"}
    authjwt_access_token_expires: timedelta = timedelta(minutes=15)
    authjwt_refresh_token_expires: timedelta = timedelta(days=3)
    REDIS_HOST_URL = os.environ.get("REDIS_HOST_URL")
    REDIS_HOST_PORT = int(os.environ.get("REDIS_HOST_PORT"))
    REDIS_HOST_PASSWORD = os.environ.get("REDIS_HOST_PASSWORD")
    
def settings():
    return Settings()
