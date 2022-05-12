from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
def custom_response(data, status_code):
    """
    Custom Response Function
    """
    return JSONResponse(content=jsonable_encoder(data), status_code=status_code)