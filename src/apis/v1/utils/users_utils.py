from src.apis.v1.models.idp_users_model import idp_users




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
    elif order_by == "first_name" and latest == True:
        order_by_query=idp_users.first_name.asc()
    elif order_by == "first_name" and latest == False:
        order_by_query=idp_users.first_name.desc()
    elif order_by == "last_name" and latest == True:
        order_by_query=idp_users.last_name.asc()
    elif order_by == "last_name" and latest == False:
        order_by_query=idp_users.last_name.desc()
    return order_by_query

def create_user_action_filter_query(search):


    if search is not None:
        filter_query = filter_query & (idp_users.username.ilike(f"%{search}%"))
 
    return filter_query