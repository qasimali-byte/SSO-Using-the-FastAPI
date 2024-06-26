import re
from src.apis.v1.routes.idp_routes import cookie,cookie_frontend

def delete_all_cookies(response, only_frontend=False):
    if only_frontend:
        cookie_frontend.delete_from_response(response)
        return response
    # try:
    #      cookie.delete_from_response(response)
    # except:
    #     pass
    try:
        response.set_cookie(
            key="cookie_idp",
            domain="attech-ltd.com",
            value="",
            max_age=0,
            path= "/",
            secure= False,
            httponly= False,
            samesite="lax"
            )
    except:
        print("error deleting cookies")

    # try:
    #     response.delete_cookie("cookie_frontend")
    # except:
    #     print("error deleting cookies")
    # try:
    #     response.delete_cookie("cookie")
    # except:
    #     print("error deleting cookies")

    return response

def create_unique_id():
    import uuid
    return uuid.uuid1()

def remove_int_from_urls(url):
    try:
        pattern = re.compile(r'/[0-9]+')
        n_url = pattern.sub('', url)
        return n_url
    except:
        return ""