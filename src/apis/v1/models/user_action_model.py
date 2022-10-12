from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from . import Base

class user_action(Base):
    __tablename__ = "user_action"
    id = Column(Integer, primary_key=True)
    idp_user_id = Column(Integer, ForeignKey('idp_users.id'))
    action_id = Column(Integer, ForeignKey("action.id"))
    app_name = Column(String(155), ForeignKey('sp_apps.sp_metadata'),nullable=True, unique=False)
    role_name = Column(String(155),nullable=True, unique=False)
    action_date = Column(DateTime, nullable=False, unique=False)
    status = Column(String(255),nullable=False, unique=False)
    action = relationship("action", uselist=False, lazy="joined")
    idp_user = relationship("idp_users", uselist=False ,lazy="joined")
    sp_app = relationship("SPAPPS", uselist=False ,lazy="joined", foreign_keys='user_action.app_name')


    def user_actions_as_dict(self):
        return {
            "id": self.id,
            "idp_user_id": self.idp_user.id,
            "idp_user_name": self.idp_user.first_name + " " + self.idp_user.last_name,
            "idp_user_email": self.idp_user.email,
            "action_id": self.action.id,
            "action_name": self.action.name,
            "action_label": self.action.label,
            "action_level": self.action.level,
            "app_name": self.app_name,
            "role_name": self.role_name,
            "action_date": self.action_date,
            "status": self.status,
            "display_name": self.sp_app.display_name if self.sp_app else "",
            "logo": self.sp_app.logo_url if self.sp_app else "",
        }