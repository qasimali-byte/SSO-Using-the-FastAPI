from src.apis.v1.helpers.customize_response import custom_response
from src.apis.v1.services.sps_service import SPSService
from src.apis.v1.validators.general_validators import ErrorResponseValidator, SuccessfulResponseValidator
from fastapi import status
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
            useremail = "umair@gmail.com"
            sps_app = SPSService(self.db).get_sps_app(useremail)
            # if sps_app:
            #     data = SuccessfulResponseValidator(message="SPS app found",status=True,data=sps_app)
            #     response = custom_response(data=data,status_code=status.HTTP_200_OK)
            #     return response

            # data = ErrorResponseValidator(message="SPS app not found",status=False)
            # response = custom_response(data=data,status_code=status.HTTP_404_NOT_FOUND)
            # return response
        except Exception as e:
            pass
            # data = ErrorResponseValidator(message=str(e),status=False)
            # response = custom_response(data=data,status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
            # return response