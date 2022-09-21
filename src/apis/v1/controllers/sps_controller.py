from select import select
from src.apis.v1.controllers.practices_controller import PracticesController
from src.apis.v1.controllers.roles_controller import RolesController
from src.apis.v1.helpers.customize_response import custom_response
from src.apis.v1.services.gender_service import GenderService
from src.apis.v1.services.practices_service import PracticesService
from src.apis.v1.services.roles_service import RolesService
from src.apis.v1.services.sps_service import SPSService
from src.apis.v1.validators.common_validators import ErrorResponseValidator, SuccessfulResponseValidator
from fastapi import status

from src.apis.v1.validators.sps_validator import FilterServiceProviderValidator, ListFilterServiceProviderValidator, ListServiceProviderValidatorOut, ListServiceProviders
from src.apis.v1.validators.user_validator import LogedInUserSPPracticeRoleValidator, SPPracticeRoleValidator, UserSelectedUnselectedSPApps
class SPSController():
    def __init__(self, db):
        self.db = db

    def create_sps(self, **kwargs):
        try:
            sps_app = SPSService(self.db).create_sps_model(**kwargs)
            if sps_app:
                data = SuccessfulResponseValidator(message="SPS app created successfully",status=True)
                response = custom_response(data=data,status_code=status.HTTP_201_CREATED)
                return response

            data = ErrorResponseValidator(message="SPS app not created",status=False)
            response = custom_response(data=data,status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
            return response
        except Exception as e:
            data = ErrorResponseValidator(message=str(e),status=False)
            response = custom_response(data=data,status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
            return response

    def get_sps(self, useremail: str):
        try:
            sps_app = SPSService(self.db).get_sps_app(useremail)
            if sps_app:
                data = ListServiceProviderValidatorOut(serviceproviders=sps_app)
                response = custom_response(data=data,status_code=status.HTTP_200_OK)
                return response

            data = ListServiceProviderValidatorOut(serviceproviders=[])
            response = custom_response(data=data,status_code=status.HTTP_200_OK)
            return response

        except Exception as e:
            data = ErrorResponseValidator(message="Some thing went wrong",status=False)
            response = custom_response(data=data,status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
            return response

    def get_all_filtered_sps_object(self, sps:list):
        try:
            if len(sps) == 0:
                data = ErrorResponseValidator(message="no service provider found against empty list",status=False)
                response = custom_response(data=data,status_code=status.HTTP_404_NOT_FOUND)
                return response , 404

            sps_data = SPSService(self.db).get_all_sps()
            if sps_data:
                filtered_sps_data = list(filter(lambda x : x.name in sps, sps_data))
                return filtered_sps_data , 200

        except Exception as e:
            print(e)
            data = ErrorResponseValidator(message=str(e),status=False)
            response = custom_response(data=data,status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
            return response , 500

    def get_all_filtered_sps(self, sps:list):
        try:
            sps = [
                'dr-iq',
                'ez-doc'
            ]
            resp = self.get_all_filtered_sps_object(sps)
            if resp[1] == 200:
                data = ListFilterServiceProviderValidator.from_orm(resp[0])
                response = custom_response(data=data,status_code=status.HTTP_200_OK)
                return response

            else:
                return resp[0]

        except Exception as e:
            print(e)
            data = ErrorResponseValidator(message=str(e),status=False)
            response = custom_response(data=data,status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
            return response

    def assign_sps_to_user(self, **kwargs):
        return SPSService(self.db).assign_sps_to_user_db(**kwargs)


    def get_practices_roles_by_apps(self,apps_list,app, selected_apps, user_id, selected_id):
        apps = SPPracticeRoleValidator(id=app["id"],name=app["sp_app_name"],
        sp_app_name=app["name"],sp_app_image=app["image"],is_selected=False,
        roles=RolesController(self.db).get_allowed_roles_by_userid(app_id=app["id"], user_id=user_id, selected_id=selected_id),
        practices=PracticesController(self.db).get_allowed_practices_by_userid(app["id"],user_id,selected_id)) 

        for iteration2 in selected_apps:
            if app["id"] == iteration2["id"]:
                apps.is_selected = True

        if apps.id == 7: ## ez login id
            apps_list.insert(0,apps.dict())

        elif apps.id == 3: ## dr iq app id
            gender_data = GenderService(self.db).get_driq_selected_gender(selected_id)
            apps.gender = gender_data
            apps_list.append(apps.dict())

        else:
            apps_list.append(apps.dict())
            
   
    def get_apps_selected_unselected(self,total_apps, selected_apps):

        apps_list=[]
        for t_data in total_apps:
            not_matched=0
            apps={}
            for s_data in selected_apps:
                if t_data['id']==s_data['id']:            
                    apps['id']=s_data["id"]
                    apps['name']=s_data["sp_app_name"]
                    apps['sp_app_name']=s_data["name"]
                    apps['sp_app_image']=s_data["image"]
                    apps['logo_url']=s_data["logo_url"]
                    apps['is_selected'] = True
                else:
                    not_matched=not_matched+1
                if(not_matched==len(selected_apps)):
                    apps['id']=t_data["id"]
                    apps['name']=t_data["sp_app_name"]
                    apps['sp_app_name']=t_data["name"]
                    apps['sp_app_image']=t_data["image"]
                    apps['logo_url']=t_data["logo_url"]
                    apps['is_selected'] = False
            apps_list.append(apps)
        
        return apps_list
   
   
            

    def get_practices_roles_by_apps_loged_in_user(self,apps_list,app, selected_apps, user_id, selected_id):
        apps = LogedInUserSPPracticeRoleValidator(id=app["id"],name=app["sp_app_name"],
        sp_app_name=app["name"],sp_app_image=app["image"],is_selected=False,
        role=RolesController(self.db).get_allowed_roles_by_userid_loged_in_user(app_id=app["id"], user_id=user_id, selected_id=selected_id),
        practices=PracticesController(self.db).get_allowed_practices_by_userid_loged_in_user(app["id"],user_id,selected_id)) 

        for iteration2 in selected_apps:
            if app["id"] == iteration2["id"]:
                pass

        if apps.id == 7: ## ez login id
            apps_list.insert(0,apps.dict())

        elif apps.id == 3: ## dr iq app id
            gender_data = GenderService(self.db).get_driq_selected_gender_loged_in_user(selected_id)
            apps.gender = gender_data
            apps_list.append(apps.dict())

        else:
            apps_list.append(apps.dict())



    def get_allowed_apps_by_userid(self, user_email, selected_email, user_id, selected_id):

        apps_list = [] # contains all the apps 
        sps_app_object = SPSService(self.db)
        total_allowed_apps = sps_app_object.get_sps_app(user_email)
        selected_apps = sps_app_object.get_sps_app(selected_email)

        if len(total_allowed_apps) == 0:
            return apps_list

        for apps_object in total_allowed_apps:
            self.get_practices_roles_by_apps(apps_list,apps_object, selected_apps, user_id, selected_id)
        return apps_list
    
    def get_selected_unselected_apps(self,selected_email):

        sps_app_object = SPSService(self.db)
        total_apps = sps_app_object.get_selected_unselected_sps_app()
        selected_apps = sps_app_object.get_sps_app(selected_email)
        if len(total_apps) == 0:
            return []
        else:
            apps_list=self.get_apps_selected_unselected(total_apps, selected_apps)
        return apps_list
    
    
    def get_allowed_apps_by_userid_for_loged_in_user(self,selected_email, user_id, selected_id):

        apps_list = [] # contains all the apps 
        sps_app_object = SPSService(self.db)
        total_allowed_apps = sps_app_object.get_sps_app(selected_email)
        selected_apps = sps_app_object.get_sps_app(selected_email)

        if len(total_allowed_apps) == 0:
            return apps_list

        for apps_object in total_allowed_apps:
            self.get_practices_roles_by_apps_loged_in_user(apps_list,apps_object, selected_apps, user_id, selected_id)
        return apps_list