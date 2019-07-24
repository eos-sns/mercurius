# !/usr/bin/python2
# coding: utf-8


""" Send emails """

import base64
import os
from email.mime.text import MIMEText

from mercurius.emails.gmail import GMailApiOAuth, send_email

HERE = os.path.dirname(os.path.realpath(__file__))
OAUTH_FOLDER = os.path.join(HERE, ".user_credentials", "gmail")
CONFIG_FOLDER = os.path.join(HERE, "config")

# email settings
EMAIL_DRIVER = GMailApiOAuth(
    "EOS",
    os.path.join(OAUTH_FOLDER, "client_secret.json"),
    os.path.join(OAUTH_FOLDER, "gmail.json")
).create_driver()
EMAIL_SENDER = "eos.cosmosns@gmail.com"
ADMIN_CONFIG_FILE = os.path.join(CONFIG_FOLDER, 'admins.json')
HELP_EMAIL = {
    "name": "Andrei Albert Mesinger",
    "email": "andrei.mesinger@sns.it"
}


def get_msg(recipient, html_content, subject):
    """
    :return: MIMEText
        Personalized message to notify user
    """

    message = MIMEText(
        "<html>" + html_content + "</html>", "html"
    )
    message["subject"] = subject
    message["to"] = str(recipient).strip()

    return {
        "raw": base64.urlsafe_b64encode(bytes(message)).decode()
    }


def send_msg(msg):
    """
    :param msg: str
        Message to send to me
    :return: void
        Sends email to me with this message
    """

    send_email(
        EMAIL_SENDER,
        msg,
        EMAIL_DRIVER
    )
