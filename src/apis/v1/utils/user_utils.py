import shortuuid

from src.apis.v1.core.project_settings import Settings


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


def image_writer(data_image):
    message = ""
    image_data = data_image["file"]
    image_name = data_image["name"]
    content_type = data_image["type"]

    if content_type in ["image/png", "image/jpg", "image/jpeg", "image/webp"]:
        message += " accepted "
    else:
        message += " Invalid image typ"
        return {"message": "There was an error,Invalid image type only png, jpg, jpeg,webp allowed"}
    resource_name = shortuuid.ShortUUID().random(length=8) + f".{content_type.split('/')[-1]}"
    with open(f"./public/assets/{resource_name}", 'wb') as f:
        f.write(image_data)

    return Settings().BASE_URL + "/image/" + resource_name