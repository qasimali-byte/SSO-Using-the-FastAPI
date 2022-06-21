

from lib2to3.pgen2.token import OP
import load_env
from sqlalchemy import and_, create_engine
from sqlalchemy.orm import sessionmaker
from typing import Generator
import sqlalchemy
from src.apis.v1.models import *
from src.apis.v1.core.project_settings import Settings
from src.apis.v1.models.sp_apps_model import SPAPPS
from src.apis.v1.models.roles_model import roles
from sqlalchemy.orm import joinedload, lazyload
from pydantic import BaseModel, Field
from typing import List,Optional


    # class Config:
    #     orm_mode = True

# class Resp(BaseModel):
#     spam: Optional[List[Spam]]
SQLALCHEMY_DATABASE_URL = Settings().DATABASE_URL
engine = create_engine(SQLALCHEMY_DATABASE_URL)
session_ = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = session_()
# join_data = db.query(SPAPPS,sp_apps_role,roles).join(sp_apps_role,SPAPPS.id == sp_apps_role.sp_apps_id).join(roles,sp_apps_role.roles_id == roles.id).all()
# print(join_data)
class ListSubRolesValidator(BaseModel):
    id: int
    name: str = Field(alias='label')

    class Config:
        orm_mode = True
    

class SubRolesValidator(BaseModel):
    id: int
    name: str 
    sub_roles: Optional[List[ListSubRolesValidator]]

class ListRolesValidator(BaseModel):
    id: int
    name: str = Field(alias='label')
    sub_roles : Optional[List[SubRolesValidator]] = []

    class Config:
        orm_mode = True


class RolesValidator(BaseModel):
    roles: Optional[List[ListRolesValidator]] = []
    
class ListSubRolesValidatorWithOutOrm(BaseModel):
    id: int
    name: str

class SubRolesValidatorWithOutOrm(BaseModel):
    id: int
    name: str 
    sub_roles: Optional[List[ListSubRolesValidatorWithOutOrm]]

class ListRolesValidatorWithOutOrm(BaseModel):
    id: int
    name: str 
    sub_roles : Optional[List[SubRolesValidatorWithOutOrm]] = []

class RolesValidatorWithOutOrm(BaseModel):
    roles: Optional[List[ListRolesValidatorWithOutOrm]] = []







def method(sp_app_id):
    # dr_iq_practices_roles_object = db.query(sp_apps_role).options(joinedload(sp_apps_role.driq_practices_role)).all()
    # for values in dr_iq_practices_roles_object:
    #     print(vars(values))

    roles = []
    roles_object = db.query(SPAPPS).options(joinedload(SPAPPS.roles)).filter(SPAPPS.id == sp_app_id).first()
    if sp_app_id == 3:
        for values in roles_object.roles:
            dr_iq_practices_roles_object = db.query(sp_apps_role).filter(and_(sp_apps_role.roles_id == values.id, sp_apps_role.sp_apps_id == 3)).options(joinedload(sp_apps_role.driq_practices_role)).first()
            sub_roles = SubRolesValidator(id=values.id,name=values.label,sub_roles=dr_iq_practices_roles_object.driq_practices_role).dict()
            roles.append(sub_roles)

        return roles
    else:
        roles = RolesValidator(roles = roles_object.roles).dict()
        return roles["roles"]
    # roles = []
    # if sp_app_id == 3:
    #     roles_object = db.query(SPAPPS).options(joinedload(SPAPPS.roles)).filter(SPAPPS.id == 3).first()
    #     for values in roles_object.roles:
    #         print(values.id)
    #         dr_iq_practices_roles_object = db.query(sp_apps_role).options(joinedload(sp_apps_role.driq_practices_role)).filter(and_(sp_apps_role.roles_id == values.id, sp_apps_role.sp_apps_id == 3)).first()
    #         sub_roles = RolesValidator(id=values.id,name=values.name,roles=dr_iq_practices_roles_object.driq_practices_role).dict()
    #         roles.append(sub_roles)
    
    # else:
    #     roles_object = db.query(SPAPPS).options(joinedload(SPAPPS.roles)).filter(SPAPPS.id == sp_app_id).first()
    #     roles = RolesValidator(id=roles_object.id,name=roles_object.name,roles=roles_object.roles).dict()
    # return roles

        # for objects in dr_iq_practices_roles_object:
        #     sub_roles = RolesValidator(id=values.id,name=values.name,roles=dr_iq_practices_roles_object.driq_practices_role).json()
        #     print(sub_roles)
# for values in data.roles:
#     values1 = db.query(sp_apps_role).filter(sp_apps_role.sp_apps_id == 3).options(joinedload(sp_apps_role.driq_practices_role)).all()
# data1 = db.query(sp_apps_role).filter(sp_apps_role.sp_apps_id == 3).options(joinedload(sp_apps_role.driq_practices_role)).all()
# print(data1)
# d = List[RolesValidator]
# x = d(list())
# resp = Resp(spam=data)
# list1 = []
# for values in data:
    
    
#     # resp = Resp(spam=values)
#     if values.name == "dr-iq":
#         values1 = db.query(sp_apps_role).filter(sp_apps_role.sp_apps_id == 3).options(joinedload(sp_apps_role.driq_practices_role)).all()
#         for values2 in values1:
#             list1.append(Spam(id=values.id,name=values.name,roles=values2.driq_practices_role).json())
        # resp = Spam(bars=values.roles)
        # print(vars(values.roles[0]))
    #     print(values[1].driq_practices_role,)
        # print(values[0].roles)
        # data1 = db.query(sp_apps_role).filter(sp_apps_role.sp_apps_id == 3).options(joinedload(sp_apps_role.driq_practices_role)).all()
        # print(vars(data1[0]))
        # print(values.id)
        # print(vars(values))
    # else:
    #     list1.append(Spam(id=values.id,name=values.name,roles=values.roles).json())

# print(resp.json())
# print(list1)
# print(vars(data[0]),vars(data[0].roles[0]))
# print(vars(data[0]))
# print(vars(data[0][1]))
# print(vars(data[0]))
# data = db.query(SPAPPS) \
# .join(sp_apps_role,SPAPPS.id == sp_apps_role.sp_apps_id).join(roles,sp_apps_role.roles_id == roles.id).all()
# print(vars(data[0]))
# for values in data:
#     print(vars(values[0]),vars(values[1]),vars(values[2]))


if __name__ == "__main__":
    d = method(1)
    print(d)
    RolesValidatorWithOutOrm(roles=d)
    print(d)