import shortuuid

from src.apis.v1.core.project_settings import Settings
from src.apis.v1.helpers.custom_exceptions import CustomException
from fastapi import status
from cryptography.fernet import Fernet

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


def get_encrypted_text(text):
    try:
        if text:
            key = Settings().FERNET_SECRET_KEY
            cipher_suite = Fernet(key)
            encoded_text = cipher_suite.encrypt(text)
            return encoded_text
            decoded_text = cipher_suite.decrypt(encoded_text)
    except Exception as e:
        print(str(e))
        return None


def get_decrypted_text(text):
    try:
        if text:
            key = Settings().fernet_secret_key
            cipher_suite = Fernet(key)
            decoded_text = cipher_suite.decrypt(text)
            return decoded_text
    except Exception as e:
        print(str(e))
        return None


def image_writer(data_image):
    message = ""
    image_data = data_image["file"]
    image_name = data_image["name"]
    content_type = data_image["type"]

    if content_type in ["image/png", "image/jpg", "image/jpeg", "image/webp"]:
        message += " accepted "
    else:
        message += " Invalid image typ"
        raise CustomException(message="There was an error,Invalid image type only png, jpg, jpeg,webp allowed - error occured in user utils", status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)

    resource_name = shortuuid.ShortUUID().random(length=8)+"_"+image_name+f".{content_type.split('/')[-1]}"
    resource_name = resource_name.replace(" ","_")
    with open(f"./public/assets/{resource_name}", 'wb') as f:
        try:
            f.write(image_data)
        except Exception as e:
            raise CustomException(message="There was an error,Error in writing image - error occured in user utils", status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)

    return "image/" + resource_name


def format_data_for_update_user_image(image) -> dict:
    """
        Format Data For Update User Controller
    """

    try:
        data_image = {}
        data_image['file'] = image.file.read()
        data_image['name'] = image.filename
        data_image['type'] = image.content_type
        return data_image

    except Exception as e:
        raise CustomException(message= f"There was an error uploading the file(s),{e} - error occured in user utils", status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)

