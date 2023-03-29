from src.apis.v1.models.user_idp_sp_apps_model import idp_sp


def get_subquery(status):

    if  status != ['All']:
        query = {idp_sp.action.in_(status)}
        return query
    elif  status == ['All']:
        query = {idp_sp.action.in_(status)}
        return query

