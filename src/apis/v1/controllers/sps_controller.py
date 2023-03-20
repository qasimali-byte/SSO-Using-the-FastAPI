from select import select
from src.apis.v1.controllers.practices_controller import PracticesController
from src.apis.v1.controllers.roles_controller import RolesController
from src.apis.v1.daos.sps_dao import SyncSpsDAO
from src.apis.v1.helpers.customize_response import custom_response
from src.apis.v1.models.sp_apps_model import SPAPPS
from src.apis.v1.services.gender_service import GenderService
from src.apis.v1.services.practices_service import PracticesService
from src.apis.v1.services.roles_service import RolesService
from src.apis.v1.services.sps_service import SPSService
from src.apis.v1.validators.common_validators import ErrorResponseValidator, SuccessfulResponseValidator
from fastapi import status

from src.apis.v1.validators.user_validator import LogedInUserSPPracticeRoleValidator, SPPracticeRoleValidator
from src.apis.v1.validators.sps_validator import FilterServiceProviderValidator, ListFilterServiceProviderValidator, ListServiceProviderValidatorOut, ListServiceProviders, ListSpAppsGeneralValidator

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
        apps = SPPracticeRoleValidator(id=app["id"],name=app["name"],
        sp_app_name=app["sp_app_name"],sp_app_image=app["image"],is_selected=False,
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
            
   
    def get_apps_selected_unselected(self,total_sp_apps, selected_sp_apps):
        
        selected_ids = {app['id']: app for app in selected_sp_apps}

        # Iterate through the total sp apps list, and create the final list of dictionaries
        final_list = []
        for app in total_sp_apps:
            # If the app is in the selected apps list, set its is_selected value based on its is_accessible value
            if app['id'] in selected_ids:
                selected_app = selected_ids[app['id']]
                app['is_selected'] = selected_app['is_accessible']
            # Otherwise, set its is_selected value to False
            else:
                app['is_selected'] = False
            # Add the app to the final list
            final_list.append({
                'id': app['id'],
                'name': app['name'],
                'sp_app_name': app['display_name'],
                'logo_url': app['logo_url'],
                'host_url': app['host_url'],
                'is_selected': app['is_selected']
            })

        return final_list
    
    def get_unaccessible_apps(self,total_apps, selected_apps):

        apps_list=[]
        for t_data in total_apps:
            not_matched=0
            apps={}
            for s_data in selected_apps:
                if t_data['id']==s_data['id']:            
                    apps['id']=s_data["id"]
                    apps['name']=s_data["name"]
                    apps['sp_app_name']=s_data["display_name"]
                    apps['logo_url']=s_data["logo_url"]
                    apps['host_url']=s_data["host_url"]
                    apps['is_selected'] = True
                else:
                    not_matched=not_matched+1
                if(not_matched==len(selected_apps)):
                    apps['id']=t_data["id"]
                    apps['name']=t_data["name"]
                    apps['sp_app_name']=t_data["display_name"]
                    apps['logo_url']=t_data["logo_url"]
                    apps['host_url']=t_data["host_url"]
                    apps['is_selected'] = False
            apps_list.append(apps)
        
        return apps_list
   
   
            

    def get_practices_roles_by_apps_loged_in_user(self,apps_list,app, selected_apps, user_id, selected_id):
        apps = LogedInUserSPPracticeRoleValidator(id=app["id"],name=app["name"],
        sp_app_name=app["sp_app_name"],sp_app_image=app["image"],is_selected=False,
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
    
    def get_spapps_status(self,selected_user_id):

        sps_app_object = SPSService(self.db)
        spapps_status = sps_app_object.get_spapps_status(selected_user_id)
        return spapps_status
    
    
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

    def get_specific_product_byappid(self, app_id:int):
        dto = SyncSpsDAO(self.db).get(filter_data={SPAPPS.is_active: True,SPAPPS.id:app_id})
        return ListSpAppsGeneralValidator.from_orm(dto).dict()
    
    def add_verified_sp_apps(self,idp_user_id,account_access_verify_validator):
        return SPSService(self.db).add_sp_app_verification_status(idp_user_id,account_access_verify_validator)
    
    def get_sp_app_by_id(self,sp_app_id):
        sp_app_data=SPSService(self.db).get_sp_app_by_id(sp_app_id)
        return sp_app_data
    
    def get_sp_apps_email(self,sp_apps_id,primary_email):
        sp_app_email=SPSService(self.db).get_sp_apps_email(sp_apps_id,primary_email)
        return sp_app_email