import os
from pathlib import Path
from dotenv import load_dotenv

env_path = Path(".") / ".env"
load_dotenv(dotenv_path=env_path)


class Settings:
    PROJECT_TITLE: str = "SSO IDP"
    PROJECT_VERSION: str = "0.0.1"
    HOST_URL: str = os.getenv("HOST_URL", "127.0.0.1")
    HOST_PORT: int = os.getenv("HOST_PORT", 8088)
    POSTGRES_USER: str = os.getenv("POSTGRES_USER","postgres")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD","faisal")
    POSTGRES_SERVER: str = os.getenv("POSTGRES_SERVER", "127.0.0.1")
    POSTGRES_PORT: str = os.getenv("POSTGRES_PORT", 5432)
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "sso_idp")
    DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"

    # SECRET_KEY: str = os.getenv("SECRET_KEY")
    # ALGORITHM = "HS256"
    # ACCESS_TOKEN_EXPIRE_MINUTES = 30
    # TEST_USER_EMAIL = "test@example.com"


settings = Settings()