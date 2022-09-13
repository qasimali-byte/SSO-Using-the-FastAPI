from src.apis.v1.models.idp_users_model import idp_users
from src.apis.v1.models.sp_apps_model import SPAPPS


def get_order_by_query(order_by,latest):

    '''
    Ascending means smallest to largest, 0 to 9, and/or A to Z and Descending means largest to smallest, 
    9 to 0, and/or Z to A. Ascending order means the smallest or first or earliest in the order will appear 
    at the top of the list: For numbers or amounts, the sort is smallest to largest.
    '''
    if order_by == "id" and latest == True:
        order_by_query=idp_users.id.asc()
    elif order_by == "id" and latest == False:
        order_by_query=idp_users.id.desc()
    if order_by == "first_name" and latest == True:
        order_by_query=idp_users.first_name.asc()
    elif order_by == "first_name" and latest == False:
        order_by_query=idp_users.first_name.desc()
    elif order_by == "last_name" and latest == True:
        order_by_query=idp_users.last_name.asc()
    elif order_by == "last_name" and latest == False:
        order_by_query=idp_users.last_name.desc()
    elif order_by == "created_date" and latest == False:
        order_by_query=idp_users.created_date.desc()
    elif order_by == "created_date" and latest == True:
        order_by_query=idp_users.created_date.asc()
    return order_by_query


def get_subquery(search,select_practices,user_status):
    # this sort of list will recieve by front end ['ez-login,dr-iq,ez-web']
    if select_practices != ['All']:
        select_practices=[value.split(',') for value in select_practices]
        select_practices=select_practices[0]

    if  search is None and select_practices ==['All'] and user_status == True:
        # Case 1
        query= {idp_users.is_active==True}
        return  query
    elif search is None and select_practices ==['All'] and user_status == False:
        # Case 2
        query= {idp_users.is_active==False}
        return  query
    elif search is None and select_practices !=['All'] and user_status == True:
        # Case 3
        query= {idp_users.is_active==True,SPAPPS.name.in_(select_practices)}
        return query
    elif search is None and select_practices !=['All'] and user_status == False:
        # Case 4
        query= {idp_users.is_active==False,SPAPPS.name.in_(select_practices)}
        return query
    elif search is not None and select_practices ==['All'] and user_status == True:
        #Case 5
        query= {idp_users.is_active==True,idp_users.username.ilike(f"%{search}%")}
        return query
    elif search is not None and select_practices ==['All'] and user_status == False:
        # Case 6
        query= {idp_users.is_active==False,idp_users.username.ilike(f"%{search}%")}
        return query
    elif search is not None and select_practices !=['All'] and user_status == True:
        query= {idp_users.is_active==True,idp_users.username.ilike(f"%{search}%"),SPAPPS.name.in_(select_practices)}
        return query
    elif search is not None and select_practices !=['All'] and user_status == False:
        # Case 8
        query= {idp_users.is_active==False,idp_users.username.ilike(f"%{search}%"),SPAPPS.name.in_(select_practices)}
        return query
    else:
        return {}

    
    
