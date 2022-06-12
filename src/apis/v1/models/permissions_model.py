from sqlalchemy import Column, Integer, String
from . import Base

class permissions(Base):
    __tablename__ = "permissions"
    """
        Permissions table to manage the permissions of the users with the roles.
    """
    id = Column(Integer, primary_key=True, index=True)
    permission = Column(String(255),nullable=False, unique=False)