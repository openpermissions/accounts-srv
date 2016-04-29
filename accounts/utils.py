# -*- coding: utf-8 -*-
# Copyright 2016 Open Permissions Platform Coalition
# 
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
# 
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
# 
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA
# 

"""
Utility methods for the accounts service.
"""
import logging
import smtplib
import html2text
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from tornado.options import options
from tornado.gen import coroutine, Return
from concurrent.futures import ThreadPoolExecutor


executor = ThreadPoolExecutor(max_workers=4)


def smtp_sendmail(host, port, user, password, send_from, send_to, message):
    """
    Sends an html email using smtp credentials in config
    :param host: smtp host
    :param port: smtp port
    :param user: smtp user
    :param password: smtp password
    :param send_from: address to send email from
    :param send_to: list of addresses to send email to
    :param message: email body
    """
    # Log warning if SMTP server not configured, but do not error
    if not (host and port and send_from and user and password):
        logging.warn('SMTP Server not configured. '
                     'Service will not be able to send emails until this is done.')
        return
    try:
        smtpserver = smtplib.SMTP(host, port)
        smtpserver.login(user, password)
        smtpserver.sendmail(send_from, send_to, message)
        smtpserver.quit()
    except smtplib.SMTPException:
        # Log smtp problems as warnings rather than errors.
        logging.warn('Email could not be sent', exc_info=True)


@coroutine
def build_mime_text(recipients, subject, message):
    """
    Puts message data into MIME format
    :param recipients: array of email addresses to send email to
    :param subject: subject of email
    :param message: body of email
    :return MIMEMultipart object
    """

    # Record the MIME types of text/plain and text/html.
    part1 = MIMEText(html2text.html2text(message), 'plain')
    part2 = MIMEText(message, 'html')

    # Attach parts into mime message container.
    body = MIMEMultipart('alternative')
    body['Subject'] = subject
    body['From'] = options.smtp_from
    body['To'] = ",".join(recipients)
    body.attach(part1)
    body.attach(part2)

    raise Return(body)


@coroutine
def send_email(recipients, subject, message):
    """
    Sends an html email using smtp credentials in config
    :param recipients: email address or array of email addresses to send email to
    :param subject: subject of email
    :param message: body of email
    """
    if not isinstance(recipients, list):
        recipients = [recipients]

    send_list = [
        address for address in recipients
        if not address.split('@')[-1] in options.blacklist_domains]

    if not send_list:
        return

    body = yield build_mime_text(send_list, subject, message)
    # Create smtp connection and send email
    yield executor.submit(
        smtp_sendmail,
        options.smtp_host,
        options.smtp_port,
        options.smtp_user,
        options.smtp_pass,
        options.smtp_from,
        send_list,
        body.as_string())
