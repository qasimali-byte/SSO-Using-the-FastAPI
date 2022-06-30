import os

from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
def custom_response(data, status_code):
    """
    Custom Response Function
    """
    return JSONResponse(content=jsonable_encoder(data), status_code=status_code)

def file_remover(file_name):
    try:
        if os.path.isfile(file_name):
            os.remove(file_name)
            return "success"
    except OSError as e:
        print("Error: %s - %s." % (e.filename, e.strerror))