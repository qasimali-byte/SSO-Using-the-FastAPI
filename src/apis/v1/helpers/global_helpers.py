from src.apis.v1.routes.idp_routes import cookie,cookie_frontend
def delete_all_cookies(response, only_frontend=False):
    if only_frontend:
        cookie_frontend.delete_from_response(response)
        return

    cookie.delete_from_response(response)
    cookie_frontend.delete_from_response(response)

def create_unique_id():
    import uuid
    return uuid.uuid1()