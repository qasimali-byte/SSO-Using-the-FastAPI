async def get_user_actions(first: int = 10, cursor: Optional[Cursor] = None, direction: Optional[str] = "forward",
        search: Optional[str] = None, role_name: Optional[str] = None,action_level:Optional[str]=None,
        start_date_time:Optional[str]=None,end_date_time:Optional[str]=None
        ) -> Connection[UserAction]:

    start_date_time = datetime.strptime(start_date_time, '%Y-%m-%d') if start_date_time is not None else None
    end_date_time = datetime.strptime(end_date_time, '%Y-%m-%d') if end_date_time is not None else None
    cursor_id = decode_user_action_id(cursor)
    if start_date_time is not None and end_date_time is not None:
        my_time = datetime.min.time()
        start_date_time  = datetime.combine(start_date_time, my_time)
        my_time = datetime.max.time()
        end_date_time  = datetime.combine(end_date_time, my_time)

    filter_query = create_user_action_filter_query(search,role_name,action_level,start_date_time,end_date_time)
    order_by_query = create_user_action_orderby_query(order_by="id")

    if direction == "forward":
        async with get_session() as s:

            sql = select(user_action.id).join(action).join(idp_users)\
            .filter(filter_query).subquery()

            count_records_query = select(func.count(user_action.id)).filter(user_action.id.in_(select(sql)))
            count_records = (await s.execute(count_records_query)).scalars().unique().one()

            sql = select(user_action).filter(user_action.id.in_(select(sql))) \
            .filter(user_action.id > cursor_id).order_by(order_by_query).limit(first+1)
            result = (await s.execute(sql)).scalars().unique()
        
        user_actions = [UserAction(**values.user_actions_as_dict()) for values in result]
        
        ## when we have no records, we return an empty list
        if len(user_actions) == 0:
            return get_zero_user_actions_data(count_records)

        edges = [
            Edge(node=UserAction.from_db_model(user_action), cursor=build_user_action_cursor(user_action))
            for user_action in user_actions 
        ]

        ## when we have reached the last page
        if (len(user_actions) > first) == False: 
            start_cursor=edges[0].cursor if edges else None
            end_cursor=edges[-1].cursor if len(edges) > 1 else None
        ## when we have not reached the last page
        else: 
            start_cursor=edges[0].cursor if edges else None
            end_cursor=edges[-2].cursor if len(edges) > 1 else None
            edges=edges[:-1]
        return Connection(
            page_info=PageInfo(
                has_previous_page=False if decode_user_action_id(edges[0].cursor) == 1 else True,
                has_next_page=len(user_actions) > first,
                start_cursor=start_cursor,
                end_cursor=end_cursor,
                per_page= first,
                page_count= math.ceil(count_records / first),
                total_records= count_records,
            ),
            edges=edges # exclude last one as it was fetched to know if there is a next page
        )

    elif direction == "backward":
        async with get_session() as s:
            sql = select(user_action.id).join(action).join(idp_users)\
            .filter(filter_query).subquery()

            count_records_query = select(func.count(user_action.id)).filter(user_action.id.in_(select(sql)))
            count_records = (await s.execute(count_records_query)).scalars().unique().one()

            sql = select(user_action).filter(user_action.id.in_(select(sql))) \
            .filter(user_action.id < cursor_id).order_by(desc(order_by_query)).limit(first)
            result = (await s.execute(sql)).scalars().unique().all()

        user_actions = [UserAction(**values.user_actions_as_dict()) for values in result]
        user_actions = sorted(user_actions, key=lambda x: x.id)
        
        ## when we have no records, we return an empty list
        if len(user_actions) == 0:
            return get_zero_user_actions_data(count_records)

        edges = [
            Edge(node=UserAction.from_db_model(user_action), cursor=build_user_action_cursor(user_action))
            for user_action in user_actions 
        ]

        return Connection(
            page_info=PageInfo(
                has_previous_page=False if decode_user_action_id(edges[0].cursor) == 1 else True,
                has_next_page=len(user_actions)+1 > first,
                start_cursor=edges[0].cursor if edges else None,
                end_cursor=edges[-1].cursor if len(edges) > 1 else None,
                per_page= first,
                page_count= math.ceil(count_records / first),
                total_records= count_records,
            ),
            edges=edges[:] # exclude last one as it was fetched to know if there is a next page
        )
