from datetime import datetime
import strawberry
from pydantic import Field, typing

@strawberry.type
class UserAction:
    id: int
    idp_user_id: typing.Optional[int]
    action_id: typing.Optional[int]
    idp_user_name: typing.Optional[str] = ""
    idp_user_email: typing.Optional[str] = ""
    action_name: typing.Optional[str] = ""
    action_label: typing.Optional[str] = ""
    action_level: typing.Optional[str] = ""
    app_name: typing.Optional[str] = ""
    action_date: typing.Optional[datetime] = Field(default_factory=datetime.now)
    display_name: typing.Optional[str] = ""
    logo: typing.Optional[str] = ""
    status: typing.Optional[str] = ""
    role_name: typing.Optional[str] = ""

    @classmethod
    def from_db_model(cls, instance):
        """Adapt this method with logic to map your orm instance to a strawberry decorated class"""
        return cls(id=instance.id,idp_user_id=instance.idp_user_id,action_id=instance.action_id,
        idp_user_name=instance.idp_user_name,idp_user_email=instance.idp_user_email,
        action_name=instance.action_name,action_label=instance.action_label,action_level=instance.action_level,
        app_name=instance.app_name,action_date=instance.action_date,status=instance.status,role_name=instance.role_name,\
                   display_name=instance.display_name,logo=instance.logo)