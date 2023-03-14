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
from .user_idp_sp_apps_model import idp_sp
from .samlusersessionmodel import SAMLUserSession
from .idp_user_types_model import idp_user_types
from .roles_model import roles
from .type_role_permissions_model import type_role_permissions
from .permissions_model import permissions
from .practices_model import practices
from .idp_users_practices_model import idp_users_practices
from .gender_model import gender
from .sp_apps_role_model import sp_apps_role
from .driq_practices_role_model import driq_practices_role
from .sp_apps_role_driq_practice_role_model import sp_apps_role_driq_practice_role
from .idp_user_apps_roles_model import idp_user_apps_roles
from .idp_users_model import idp_users
from .action_model import action
from .user_action_model import user_action
from .action_api_model import action_api
from .api_model import api
from .role_api_model import role_api
from .two_factor_authentication_model import two_factor_authentication
from .idp_users_sp_apps_email_model import idp_users_sp_apps_email
