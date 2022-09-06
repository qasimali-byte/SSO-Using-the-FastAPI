import email
import imaplib
import lxml.html
try:
    from ..api_v1.global_test_variables import TestVariables
    user = TestVariables.demo_forgot_password_email
except:
    user = "email.tester.asad@gmail.com"
gmail_pass = "btlmnwdcnxwfclgf"
host = "imap.gmail.com"


def read_email_from_gmail(count=2, contain_body=False):
    # Create server and login
    mail = imaplib.IMAP4_SSL(host)
    mail.login(user, gmail_pass)

    # Using SELECT to chose the e-mails.
    res, messages = mail.select('INBOX')

    # Caluclating the total number of sent Emails
    messages = int(messages[0])

    # Iterating over the sent emails
    for i in range(messages, messages - count, -1):
        # RFC822 protocol
        res, msg = mail.fetch(str(i), "(RFC822)")
        for response in msg:
            if isinstance(response, tuple):
                msg = email.message_from_bytes(response[1])

                # Store the senders email
                sender = msg["From"]
                if sender == "attech.ez.login@gmail.com":
                    # Store subject of the email
                    subject = msg["Subject"]
                    when    = msg["Date"]
                    # Store Body
                    body = ""
                    temp = msg
                    if temp.is_multipart():
                        for part in temp.walk():
                            ctype = part.get_content_type()
                            cdispo = str(part.get('Content-Disposition'))

                            # skip text/plain type
                            if ctype == 'text/html' :#and 'attachment' not in cdispo:
                                body = part.get_payload(decode=True)  # decode
                                break
                    else:
                        body = temp.get_payload(decode=True)

                    # Print Sender, Subject, Body
                    print("-" * 50)  # To divide the messages
                    print("From    : ", sender)
                    print("Subject : ", subject)
                    print("When : ", when)
                    if (contain_body):
                        return get_href_from_email_content(body.decode())


    mail.close()
    mail.logout()

def get_href_from_email_content(html_content):
    """returns href from "a" (anchor) tag"""
    tree = lxml.html.fromstring(html_content)
    href_list = tree.xpath('//a/@href')
    return href_list[0] if len(href_list)>0 else None

if __name__ == "__main__":
    email_verification_url = read_email_from_gmail(1, True)
    print(email_verification_url)