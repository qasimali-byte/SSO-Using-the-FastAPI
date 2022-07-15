import os
import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_email(url, recipient, attachment=None):
    try:
        mail_content = f"Hi,\n \tPlease verify your account by visiting the following link.\n\n {url}\n\n Thank you."
        # The mail addresses and password
        sender_address = os.environ.get("EMAIL_SENDER")
        sender_pass = os.environ.get("EMAIL_SENDER_PASSWORD")
        # Setup the MIME
        message = MIMEMultipart()
        message['From'] = sender_address
        message['To'] = recipient
        message['Subject'] = os.environ.get("EMAIL_SUBJECT")
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

