import smtplib, ssl
import dotenv
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

dotenv.load_dotenv()

MAIL_FROM_ADDRESS = os.getenv("MAIL_FROM_ADDRESS")
MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
MAIL_PORT = os.getenv("MAIL_PORT")

def send_email(receivers, subj, html) :
    if not receivers :
        return
    message = MIMEMultipart("alternative")
    message["Subject"] = subj
    message["From"] = MAIL_FROM_ADDRESS
    message["To"] = ", ".join(receivers)

    message.attach(MIMEText(html, "html"))

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", MAIL_PORT, context=context) as server:
        server.login(MAIL_FROM_ADDRESS, MAIL_PASSWORD)
        server.sendmail(
            MAIL_FROM_ADDRESS, receivers, message.as_string()
        )