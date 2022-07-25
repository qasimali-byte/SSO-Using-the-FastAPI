from sqlalchemy import func, select

from src.apis.v1.models.user_action_model import user_action


async def get_count_records(db_connection):
    count_records_query = select(func.count(user_action.id))
    count_records = (await db_connection.execute(count_records_query)).scalars().unique().one()
    yield count_records