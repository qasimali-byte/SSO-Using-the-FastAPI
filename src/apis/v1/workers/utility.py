import os
import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_email(url, recipient, attachment=None):
    try:
        print("===================================================")
        print("                Email Task Started                 ")
        print("===================================================")

        html = f"""<html>
          <body style="font-family: 'Muli',sans-serif;">
            <p>Hi,</p>
            <br style = "line-height:70px;"> 
            <p>You have requested to signup using this email. Please verify it
               by clicking the following button.<br>Please ignore it if that were not you.
            </p>
            <br>
            <br>
            <div style="margin: 0; position: absolute; top: 50%; left: 50%; -ms-transform: translate(-50%, -50%); transform: translate(-50%, -50%);" >
                 <a href="{url}"><button style="background-color: turquoise; cursor: pointer;;border:\
                 none; border-radius: 5px; color: #333; /* Dark grey */ padding: 15px 32px">Click here to verify</button>
                 </a>
             </div>
            <br style = "line-height:150px;"> 
            <p>Thank you.</p>
          </body>
        </html>"""
        mail_content = MIMEText(html, "html")
        # The mail addresses and password
        # The mail addresses and password
        sender_address = os.environ.get("EMAIL_SENDER")
        sender_pass = os.environ.get("EMAIL_SENDER_PASSWORD")
        # Setup the MIME
        message = MIMEMultipart()
        message['From'] = sender_address
        message['To'] = recipient
        message['Subject'] = os.environ.get("EMAIL_SUBJECT")
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
        print("===================================================")
        print(f"      Success: {recipient}")
        print("===================================================")
        return True
    except Exception as e:
        print(str(e))
        return False
