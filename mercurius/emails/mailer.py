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
HELP_EMAILS = [
    {
        "name": "Andrei Albert Mesinger",
        "email": "andrei.mesinger@sns.it"
    }
]
HELP_EMAILS_HTML = [
    '<a href="mailto:' + x['email'] + '">' + x['name'] + '</a>'
    for x in HELP_EMAILS
]


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


def notify_user(raw_message, recipient, name_surname, subject):
    """
    :param raw_message: str
        HTML message
    :param recipient: str
        Email of recipient
    :return: bool
        True iff successful notification
    """

    raw_message = "Dear {},<br><br>".format(name_surname) + raw_message
    raw_message += "<br><br>Best regards,<br><br>EOS developers"
    msg = get_msg(recipient, raw_message, subject)
    send_msg(msg)


def notify_user_of_bad_handle(recipient, name_surname):
    help_emails = 'or'.join(HELP_EMAILS_HTML)
    msg = "EOS is not able to parse your request. It seems the input is invalid. Please retry in a few hours.<br>" \
          "If the problem persists, please contact {}.".format(help_emails)
    notify_user(msg, recipient, name_surname, "EOS | bad request")


def notify_user_of_good_input_bad_handle(recipient, name_surname):
    help_emails = 'or'.join(HELP_EMAILS_HTML)
    msg = "EOS is not able to handle your request. It's us not you. Please retry in a few hours.<br>" \
          "If the problem persists, please contact {}.".format(help_emails)
    notify_user(msg, recipient, name_surname, "EOS | bad request")


def notify_user_of_good_request(recipient, name_surname, eta):
    eta_time = eta['long time']
    msg = "EOS has parsed correctly your request. It will be processed.<br>" \
          "You will receive another email with the link to download the " \
          "output.".format(eta_time)
    notify_user(msg, recipient, name_surname, "EOS | start")


def notify_user_of_download(recipient, name_surname, download_info):
    download_link = download_info['link']
    download_timeout = download_info['timeout']

    msg = "EOS has finished fetching the data. Here is the <a href='{}'>download link</a> to download the data.<br>" \
          "Be warned that the files will be deleted {}.".format(download_link, download_timeout)
    notify_user(msg, recipient, name_surname, "EOS | download")
