def format_data_for_create_user(user_data) -> tuple:
    """
        Format Data For Create User Controller
    """

    apps = user_data['apps']
    apps_ids_list, duplicate_apps_check  = [] , {}
    practices_ids_list, duplicate_practices_check = [] ,{}
    selected_roles_list = []
    for app in apps:
        if app['id'] not in duplicate_apps_check:
            duplicate_apps_check[app['id']] = 1
            apps_ids_list.append(app["id"])
        
        for practice in app["practices"]:
            if practice['id'] not in duplicate_practices_check:
                duplicate_practices_check[practice['id']] = 1
                practices_ids_list.append(practice["id"])

        
        selected_roles_tuple = tuple([app["id"],app["role"]["id"],app["role"]["sub_role"]])
        selected_roles_list.append(selected_roles_tuple)

    return apps_ids_list, practices_ids_list, selected_roles_list