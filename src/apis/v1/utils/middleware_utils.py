from contextlib import contextmanager
import json

from redis import Redis

from src.apis.v1.controllers.action_controller import ActionController

from src.apis.v1.db.session import get_db

class async_iterator_wrapper:
    def __init__(self, obj):
        self._it = iter(obj)
    def __aiter__(self):
        return self
    async def __anext__(self):
        try:
            value = next(self._it)
        except StopIteration:
            raise StopAsyncIteration
        return value

def success_status_codes():
    return (200,201,202,204,307)

def error_status_code():
    return (409,500,501)

def get_status_of_api(status_code=None):
    if status_code in success_status_codes():
        return "successfull"
    elif status_code in error_status_code():
        return "unsuccessfull"
    else:
        return None

async def get_response_body(response):                   
    # Consuming FastAPI response and grabbing body here
    resp_body = [section async for section in response.__dict__['body_iterator']]
    # Repairing FastAPI response
    response.__setattr__('body_iterator', async_iterator_wrapper(resp_body))

    # Formatting response body for logging
    try:
        resp_body = json.loads(resp_body[0].decode())
    except:
        resp_body = str(resp_body)

    return resp_body

async def store_logs_db(authorize,response,method,url):
    """
        Store the logs in data base according to the status code
    """
    status_code = response.status_code
    status_of_api = get_status_of_api(status_code)
    if status_of_api:
        resp_body = await get_response_body(response)
        with contextmanager(get_db)() as db:
            ActionController(db).store_logs_db(authorize,resp_body,method,url,status_of_api)
                    
