from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

"""
    Registering Tables in the database
"""
from .serviceprovidersmodel import Sps
from .usermodel import User
from .usersessionmodel import UserSession
from .idp_users_model import idp_users
from .sp_apps_model import SPAPPS
from .user_idp_sp_apps_model import user_idp_sp_app, idp_sp
from .samlusersessionmodel import SAMLUserSession
from .idp_user_types_model import idp_user_types
from .roles_model import roles
from .user_role_model import idp_user_role