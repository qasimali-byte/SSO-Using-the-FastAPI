from datetime import datetime
from sqlalchemy import desc, func, select
from src.apis.v1.models.action_model import action
from src.apis.v1.models.idp_users_model import idp_users
from src.apis.v1.models.user_action_model import user_action
from src.graphql.scalars.pagination_scalar import Connection, PageInfo


def create_user_action_filter_query(search,user_email,role_name,action_level,start_date_time,end_date_time):

    filter_query = user_action.id != None
    if search is not None:
        filter_query = filter_query & (idp_users.username.ilike(f"%{search}%"))
    if user_id is not None:
        filter_query = filter_query & (idp_users.email == user_email)
    if role_name is not None:
        filter_query = filter_query & (user_action.role_name == role_name)
    if action_level is not None:
        filter_query = filter_query & (action.level == action_level)
    if start_date_time is not None and end_date_time is not None:
        filter_query = filter_query & (user_action.action_date.between(start_date_time, end_date_time))

    return filter_query

def create_user_action_orderby_query(order_by):
    if order_by == "id":
        order_by_query = user_action.id
    elif order_by == "username":
        order_by_query = idp_users.username
    elif order_by == "action":
        order_by_query = action.name
    elif order_by == "role":
        order_by_query = user_action.role_name
    elif order_by == "status":
        order_by_query = user_action.status
    elif order_by == "time":
        order_by_query = user_action.action_date
    else:
        order_by_query = user_action.id
    
    return order_by_query

def get_zero_user_actions_data(count_records):
    return Connection(edges=[], page_info=PageInfo(
    has_next_page=False,
    has_previous_page=False,
    start_cursor=None,
    end_cursor=None,
    page_count=0,
    per_page=0,
    total_records=count_records,
    ))

def get_filtered_results_query(filter_query):
    sql = select(user_action.id).join(action).join(idp_users)\
    .filter(filter_query).subquery()
    return sql

async def get_filtered_records_count(db,sql):

    count_records_query = select(func.count(user_action.id)).filter(user_action.id.in_(select(sql)))
    count_records = (await db.execute(count_records_query)).scalars().unique().one()
    return count_records

async def get_useraction_records_count(db):
    count_records_query = select(func.max(user_action.id))
    count_records = (await db.execute(count_records_query)).scalars().unique().one()
    return count_records

def get_start_and_end_date_time(start_date_time,end_date_time):
    start_date_time = datetime.strptime(start_date_time, '%Y-%m-%d') if start_date_time is not None else None
    end_date_time = datetime.strptime(end_date_time, '%Y-%m-%d') if end_date_time is not None else None

    if start_date_time is not None and end_date_time is not None:
        my_time = datetime.min.time()
        start_date_time  = datetime.combine(start_date_time, my_time)
        my_time = datetime.max.time()
        end_date_time  = datetime.combine(end_date_time, my_time)
        
    return start_date_time,end_date_time