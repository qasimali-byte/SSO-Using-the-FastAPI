from src.apis.v1.controllers.async_sps_controller import AsyncSpsController
from src.apis.v1.helpers.customize_response import custom_response
from src.apis.v1.helpers.filter_List_dictionaries import reduce_list_dictionaries
from src.apis.v1.validators.auth_validators import EmailValidatorError, EmailValidatorOut
from src.packages.service_providers.email_checker.email_checker import EmailChecker
from fastapi import status

class AsyncAuthController:

    def __init__(self, db):
        self.db = db

    async def find_user_in_other_products(self, email):
        get_all_products = await AsyncSpsController(self.db).get_all_sps_product()
        all_products_with_status = await EmailChecker().call_products(get_all_products)
        filtered_products = reduce_list_dictionaries(all_products_with_status,'is_found', True)
        if filtered_products:
            data = EmailValidatorOut(
                message= "redirection",
                verification= False, 
                roles=[], 
                email= email,
                data=filtered_products,
                statuscode=status.HTTP_308_PERMANENT_REDIRECT
                )
            response = custom_response(data=data,status_code=status.HTTP_308_PERMANENT_REDIRECT)
            return response

        data = EmailValidatorError(
            message= "invalid email",
            verification=False,
            statuscode=status.HTTP_422_UNPROCESSABLE_ENTITY 
        )
        response = custom_response(data=data,status_code=422)
        return response
        