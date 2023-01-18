"""prefork worker doesn't work in windows , so we have to use (-P solo) or (-P eventlet)\
as following:
celery -A celery_worker worker --loglevel=INFO -P eventlet
"""
import math
import os
import time
import random
from celery import Celery
import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import load_env
from jinja2 import Environment, FileSystemLoader
import requests
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders




def send_email(mail_content, recipient, attachment, subject_env):
    try:
        sender_address = os.environ.get("EMAIL_SENDER")
        sender_pass = os.environ.get("EMAIL_SENDER_PASSWORD")
        # Set up the MIME
        message = MIMEMultipart()
        message['From'] = sender_address
        message['To'] = recipient
        message['Subject'] = os.environ.get(subject_env)
        # The body and the attachments for the mail
        message.attach(mail_content)
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
        return False


def email_sender_core(mail_content, recipient, attachment):
    return send_email(mail_content, recipient, attachment, "EMAIL_SUBJECT")

def super_admin_email_sender_core(mail_content, recipient, attachment):
    return send_email(mail_content, recipient, attachment, "SUPER_ADMIN_EMAIL_SUBJECT")


def populate_html_file(url, user_name):
    base_url = f"{os.environ.get('SSO_BACKEND_URL')}api/v1/image/"
    if not "http" in base_url:
        base_url = "http://" + base_url
    environment = Environment(loader=FileSystemLoader("templates/"))
    template = environment.get_template("email.html")
    return template.render(user_activation_url=url, base_url=base_url, user_name=user_name)
    # # print(base_url)
    # with open('email.html', 'wb') as f:
    #     f.write(html_.encode())
    #     # f.truncate()


def populate_super_admin_html_file( user_name,user_role,user_number,base_url):
    base_url = f"{os.environ.get('SSO_BACKEND_URL')}api/v1/image/"
    if not "http" in base_url:
        base_url = "http://" + base_url
    environment = Environment(loader=FileSystemLoader("templates/"))
    template = environment.get_template("super_admin_email.html")
    return template.render( base_url=base_url, user_name=user_name,user_role=user_role,user_updated_number=user_number)




def populate_html_file_otp(user_data):
    environment = Environment(loader=FileSystemLoader("templates/"))
    template = environment.get_template("otp_mail.html")
    return template.render(user_data=user_data)


def populate_html_file_otp_products(user_data,base_url):
    environment = Environment(loader=FileSystemLoader("templates/"))
    template = environment.get_template("otp_mail_products.html")
    html_ =  template.render(user_data=user_data,base_url=base_url)
    with open('otp_mail_products.html', 'wb') as f:
            f.write(html_.encode())
            # f.truncate()
    return html_

def remove_file(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)


def wait_until_found_file(file_path):
    counter = 0
    while not os.path.exists(file_path):
        print(f"\t{file_path} not found")
        time.sleep(.5)
        counter+=1
        if counter==20:
            break

    if os.path.isfile(file_path):
        print(f"\tSuccess {file_path} found")
        file_ = open(file_path)
        return file_
    else:
        raise ValueError("%s isn't a file!" % file_path)


def send_otp(user_data, attachment=None):
    try:
        print("===================================================")
        print("           Create User OTP Task Started            ")
        print("===================================================")
        recipient = user_data["recipient"]
        base_url = f"{os.environ.get('SSO_BACKEND_URL')}api/v1/"
        html_ = populate_html_file_otp_products(user_data, base_url)
        mail_content = MIMEText(html_, "html")
        print("=======================Status======================")
        if email_sender_core(mail_content=mail_content, recipient=recipient, attachment=False):
            print(f"       Success: {recipient}")
        else:
            print(f"       Failed: {recipient}")
        print("===================================================")
        return True
    except Exception as e:
        print(str(e))
        return False


def send_otp_products(user_data, attachment=None):
    try:
        print("===================================================")
        print("                OTP Products Task Started          ")
        print("===================================================")
        recipient = user_data["recipient"]
        base_url = f"{os.environ.get('SSO_BACKEND_URL')}api/v1/"
        # email only renders png not svg
        [p.update((k, p["logo"].replace("svg", "png")) for k, v in p.items() if k == "logo") for p in
         user_data["products"]]
        html_ = populate_html_file_otp_products(user_data,base_url)
        mail_content = MIMEText(html_, "html")
        print("=======================Status======================")
        if email_sender_core(mail_content=mail_content,recipient=recipient,attachment=False):
            print(f"      Success: {recipient}")
            print('otp======= ',user_data["otp"])
        else:
            print(f"      Failed: {recipient}")
        print("===================================================")
        return True
    except Exception as e:
        print(str(e))
        return False


def send_email_user(url, recipient, user_name, attachment=None):
    try:
        print("===================================================")
        print("                Email Task Started                 ")
        print("===================================================")

        html_ = populate_html_file(url, user_name)
        mail_content = MIMEText(html_, "html")
        print("=====================Status=========================")
        if email_sender_core(mail_content=mail_content, recipient=recipient, attachment=False):
            print(f"      Success: {recipient}")
        else:
            print(f"      Failed: {recipient}")
        print("===================================================")
        return True
    except Exception as e:
        print(str(e))
        return False







def super_admin_email(user_name,created_by,contact_no, user_role, attachment=None):
    try:
        print("===================================================")
        print("           Send acknowledgement email to Super Admin            ")
        print("===================================================")
        base_url = f"{os.environ.get('SSO_BACKEND_URL')}api/v1/"
        html_ = populate_super_admin_html_file(base_url=base_url,user_name=user_name,user_role=user_role,user_number=contact_no)
        mail_content = MIMEText(html_, "html")
        print("=======================Status======================")
        if super_admin_email_sender_core(mail_content=mail_content, recipient=created_by, attachment=False):
            print(f"       Success: ")
        else:
            print(f"       Failed: ")
        print("===================================================")
        return True
    except Exception as e:
        print(str(e))
        return False




def send_otp_sms(user_data):
    """
       input  : contact_no, OTP
       output : True / False
       Description: To send OTP to contact_no using SMS API
    """
    print("\nCelery (send_otp_sms): ", user_data)
    try:
        raw_json = {"phone_number": user_data['contact_no'], "message": user_data['otp']}
        sms_api_url = os.environ.get('SMS_API_URL')
        res = requests.post(url=sms_api_url, json=raw_json)
        if res.status_code == 200:
            print("OTP sent via SMS")
            return True
    except Exception as err:
        raise ValueError(err)

celery = Celery(__name__)
celery.conf.broker_url = os.environ.get("CELERY_BROKER_URL", "redis://redis:6379/0")
celery.conf.result_backend = os.environ.get("CELERY_RESULT_BACKEND", "redis://redis:6379/0")


@celery.task(name="email_sender")
def email_sender(user_verification_url, user_email, user_name):
    return send_email_user(url=user_verification_url, recipient=user_email, user_name=user_name)




@celery.task(name="super_admin email_sender")
def super_admin_email_sender(user_name,created_by,contact_no, user_role):
    return super_admin_email(user_name,created_by,contact_no, user_role)


@celery.task(name="otp_sender")
def otp_sender(user_data):
    return send_otp(user_data=user_data)


@celery.task(name="otp_sender_products")
def otp_sender_products(user_data):
    return send_otp_products(user_data=user_data)


@celery.task(name="otp_sms_sender")
def otp_sms_sender(user_data):
    return send_otp_sms(user_data)


if __name__ == "__main__":
    # data = {'name': 'Asad', 'recipient': 'asadbukharee@gmail.com', 'app': 'DR IQ', 'otp': '945369', 'expires': '08:33:14 PM 29 Sep, 2022', 'logo': 'http://dev-sso-app.attech-ltd.com/api/v1/image/EZLOGO.svg'}
    user_data = {'name': 'There', 'recipient': 'user1@example.com',
     'products': [{'id': 1, 'name': 'EZ DOC', 'logo': 'image/EZDOC.svg'},
                  {'id': 2, 'name': 'EZ NAV', 'logo': 'image/EZNAV.svg'},
                  {'id': 3, 'name': 'DR.iQ', 'logo': 'image/DRIQ.svg'},
                  {'id': 6, 'name': 'EZ WEB', 'logo': 'image/EZWEBT.svg'},
                  {'id': 4, 'name': 'EZ ANALYTICS', 'logo': 'image/EZANALYTICS.svg'}], 'otp': '5609',
     'expires': '02:47:51 PM 04 Oct, 2022'}

    # otp_sender_products(user_data=user_data)
    # print(user_data)
    # [p.update((k, p["logo"].replace("svg","png")) for k, v in p.items() if k=="logo") for p in user_data["products"]]
    print(super_admin_email_sender())
    # print(user_data)