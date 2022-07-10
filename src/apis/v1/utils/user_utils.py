import base64
import logging
import traceback
from email import encoders
from email.mime.base import MIMEBase

import shortuuid
from src.apis.v1.core.project_settings import Settings
from src.apis.v1.helpers.custom_exceptions import CustomException
from fastapi import status
from cryptography.fernet import Fernet
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def format_data_for_create_user(user_data) -> tuple:
    """
        Format Data For Create User Controller
    """

    apps = user_data['apps']
    apps_ids_list, duplicate_apps_check = [], {}
    practices_ids_list, duplicate_practices_check = [], {}
    selected_roles_list = []
    for app in apps:
        if app['id'] not in duplicate_apps_check:
            duplicate_apps_check[app['id']] = 1
            apps_ids_list.append(app["id"])

        for practice in app["practices"]:
            if practice['id'] not in duplicate_practices_check:
                duplicate_practices_check[practice['id']] = 1
                practices_ids_list.append(practice["id"])

        selected_roles_tuple = tuple([app["id"], app["role"]["id"], app["role"]["sub_role"]])
        selected_roles_list.append(selected_roles_tuple)

    return apps_ids_list, practices_ids_list, selected_roles_list


def get_encrypted_text(text):
    try:
        # convert integer etc to string firsts
        txt = str(text)
        # get the key from settings
        cipher_suite = Fernet(Settings().FERNET_SECRET_KEY)  # key should be byte
        # #input should be byte, so convert the text to byte
        encrypted_text = cipher_suite.encrypt(txt.encode('ascii'))
        # encode to urlsafe base64 format
        encrypted_text = base64.urlsafe_b64encode(encrypted_text).decode("ascii")
        return encrypted_text
    except Exception as e:
        # log the error if any
        logging.getLogger("error_logger").error(traceback.format_exc())
        return None


def get_decrypted_text(text):
    try:
        # base64 decode
        if text:
            txt = base64.urlsafe_b64decode(text)
            cipher_suite = Fernet(Settings.FERNET_SECRET_KEY)
            decoded_text = cipher_suite.decrypt(txt).decode("ascii")
            return decoded_text
        else:
            return None

    except Exception as e:
        # log the error
        logging.getLogger("error_logger").error(traceback.format_exc())
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
        raise CustomException(
            message="There was an error,Invalid image type only png, jpg, jpeg,webp allowed - error occured in user utils",
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)

    resource_name = shortuuid.ShortUUID().random(length=8) + "_" + image_name + f".{content_type.split('/')[-1]}"
    resource_name = resource_name.replace(" ", "_")
    with open(f"./public/assets/{resource_name}", 'wb') as f:
        try:
            f.write(image_data)
        except Exception as e:
            raise CustomException(message="There was an error,Error in writing image - error occured in user utils",
                                  status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)

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
        raise CustomException(message=f"There was an error uploading the file(s),{e} - error occured in user utils",
                              status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)


def send_email(url, recipient, attachment=None):
    try:
        recipient = "asadbukharee@gmail.com"
        mail_content = f"Hi,\n \tPlease verify your account by visiting the following link.\n\n {url}\n\n Thank you."
        # The mail addresses and password
        sender_address = Settings().EMAIL_SENDER
        sender_pass = Settings().EMAIL_SENDER_PASSWORD
        # Setup the MIME
        message = MIMEMultipart()
        message['From'] = sender_address
        message['To'] = recipient
        message['Subject'] = Settings().EMAIL_SUBJECT
        # The body and the attachments for the mail
        message.attach(MIMEText(mail_content, 'plain'))
        # attach files if given
        if attachment:
            attach_file = open(attachment, 'rb')  # Open the file as binary mode
            payload = MIMEBase('application', 'octate-stream')
            payload.set_payload((attach_file).read())
            encoders.encode_base64(payload)  # encode the attachment
            # add payload header with filename
            payload.add_header('Content-Decomposition', 'attachment', filename=attachment.split("\"")[-1])
            message.attach(payload)
        # Create SMTP session for sending the mail
        session = smtplib.SMTP('smtp.gmail.com', 587)  # use gmail with port
        session.starttls()  # enable security
        session.login(sender_address, sender_pass)  # login with mail_id and password
        text = message.as_string()
        session.sendmail(sender_address, recipient, text)
        session.quit()
        return True
    except Exception as e:
        print(str(e))
        return False
