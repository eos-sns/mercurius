# !/usr/bin/python
# coding: utf_8


""" Use GMail APIs from python """

import smtplib


def auth_smtp(user, password, server_url, port):
    server = smtplib.SMTP_SSL(server_url, port)
    if server and server.ehlo():
        server.login(user, password)
        return server
    else:
        raise ValueError('Cannot connect to {}:{}'.format(server_url, port))


def send_email(sender, recipient, mime_msg, smtp_server):
    smtp_server.sendmail(
        sender,
        recipient,
        mime_msg.as_string()
    )
