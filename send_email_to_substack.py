# send_email_to_substack.py

import os
import smtplib
from email.message import EmailMessage

def send_email_to_substack(title, content):
    gmail_user = os.getenv("GMAIL_USER")
    gmail_pass = os.getenv("GMAIL_APP_PASSWORD")
    substack_email = os.getenv("SUBSTACK_EMAIL")  # yourblog.draft@substack.com

    if not all([gmail_user, gmail_pass, substack_email]):
        raise EnvironmentError("Missing one or more required env vars: GMAIL_USER, GMAIL_APP_PASSWORD, SUBSTACK_EMAIL")

    msg = EmailMessage()
    msg["Subject"] = title
    msg["From"] = gmail_user
    msg["To"] = substack_email
    msg.set_content(content)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(gmail_user, gmail_pass)
        smtp.send_message(msg)

    print("📬 Email sent to Substack draft inbox.")
