import base64
import math

from src.apis.v1.models.user_action_model import user_action
from sqlalchemy import desc, select
from src.graphql.scalars.user_action_scalar import UserAction
from src.graphql.scalars.pagination_scalar import PageInfo, Connection, Edge
from typing import Optional
from src.graphql.utils.user_action_utils import create_user_action_filter_query, create_user_action_orderby_query, get_filtered_records_count, get_filtered_results_query, get_start_and_end_date_time, get_useraction_records_count, get_zero_user_actions_data

def build_user_action_cursor(object: int):
    """Adapt this method to build an *opaque* ID from an instance"""
    objectid = f"{object.id}".encode("utf-8")
    decoded_valued = base64.b64encode(objectid).decode()
    return decoded_valued

Cursor = str
def decode_user_action_id(cursor: Optional[Cursor]):
    """Adapt this method to decode an *opaque* ID into an instance"""
    if cursor is not None:
        base64_bytes = cursor.encode('utf-8"')
        object_bytes = base64.b64decode(base64_bytes)
        object_id = object_bytes.decode('utf-8"')
        return int(object_id)
    return 0

async def get_user_actions(db,first: int, cursor: Optional[Cursor], direction: Optional[str],
        search: Optional[str] = None,user_id = None, role_name: Optional[str] = None,action_level:Optional[str]=None,
        start_date_time:Optional[str]=None,end_date_time:Optional[str]=None):

    start_date_time, end_date_time = get_start_and_end_date_time(start_date_time, end_date_time)
    filter_query = create_user_action_filter_query(search, user_id, role_name,action_level,start_date_time,end_date_time)
    order_by_query = create_user_action_orderby_query(order_by="id")
    sub_query_filtered_results = get_filtered_results_query(filter_query)
    total_records_count = await get_filtered_records_count(db, sub_query_filtered_results)
    max_id_without_query = await get_useraction_records_count(db)

    if total_records_count == 0:
        return get_zero_user_actions_data(total_records_count)

    if cursor is None:
        cursor_id  = max_id_without_query
    else:
        cursor_id = decode_user_action_id(cursor)
    

    if direction == "forward":

        sql = select(user_action).filter(user_action.id.in_(select(sub_query_filtered_results))) \
        .filter(cursor_id >= user_action.id).order_by(desc(order_by_query)).limit(first+1)
        result = (await db.execute(sql)).scalars().unique().all()
        returned_records_count = len(result)

        user_actions = [UserAction(**values.user_actions_as_dict()) for values in result]

        edges = [
            Edge(node=UserAction.from_db_model(user_action), cursor=build_user_action_cursor(user_action))
            for user_action in user_actions 
        ]
        return Connection(
            page_info=PageInfo(
                has_previous_page=False if (cursor is None) else True,
                has_next_page=True if first+1 <= returned_records_count else False,
                start_cursor=edges[0].cursor if (edges and cursor is not None) else None,
                end_cursor=edges[-1].cursor if (len(edges) > 1 and (first+1 <= returned_records_count)) else None ,
                per_page= first,
                page_count= math.ceil(total_records_count / first),
                total_records= total_records_count,
            ),
            edges=edges[:first]
        )

    elif direction == "backward":

        sql = select(user_action).filter(user_action.id.in_(select(sub_query_filtered_results))) \
        .filter(cursor_id < user_action.id).order_by(order_by_query).limit(first+1)
        result = (await db.execute(sql)).scalars().unique().all()
        returned_records_count = len(result)
        user_actions = [UserAction(**values.user_actions_as_dict()) for values in result]
        user_actions = reversed(user_actions)

        edges = [
            Edge(node=UserAction.from_db_model(user_action), cursor=build_user_action_cursor(user_action))
            for user_action in user_actions 
        ]
        
        return Connection(
            page_info=PageInfo(
                has_previous_page=False if (returned_records_count  < first + 1) else True,
                has_next_page=True if (returned_records_count  <= first + 1) else False,
                start_cursor=edges[1].cursor if ((edges) and (returned_records_count  >= first + 1)) else None,
                end_cursor=cursor if len(edges) > 1 else None ,
                per_page= first,
                page_count= math.ceil(total_records_count / first),
                total_records= total_records_count,
            ),
            edges=edges if returned_records_count  < first + 1 else edges[1:]
        
        )