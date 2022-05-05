import enum
class Constants(enum.Enum):
    """
    Constants class
    """
    # General
    DEBUG = False
    # Logging
    LOG_LEVEL = "INFO"
    LOG_FILE = "log.txt"
    # Database
    DB_FILE = "database.db"
    # Server
    SERVER_IP = ""
    SERVER_PORT = 8080
    # Security
    SECRET_KEY = "secret"
    # Templates
    login_template = "loginform.html"
