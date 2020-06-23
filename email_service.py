import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

SSL_PORT = 465


def send_email(receiver_email, message, subject, smtp_config):
    smtp_server = smtp_config.get("server", None)
    sender_email = smtp_config.get("email", None)
    sender_password = smtp_config.get("password", None)

    if (not smtp_server or not sender_email or not sender_password):
        raise "Invalid config exception!"

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL(smtp_server, SSL_PORT, context=context) as server:
        server.login(sender_email, sender_password)

        msg = MIMEMultipart()

        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = subject

        msg.attach(MIMEText(message, 'plain'))

        server.send_message(msg)
