# -*- coding: utf-8 -*-
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

from functools import partial

from mock import patch, call

import accounts.utils
import smtplib
from tornado.ioloop import IOLoop


def add_options(options):
    options.smtp_host = 'test host'
    options.smtp_port = 123
    options.smtp_user = 'test user'
    options.smtp_pass = 'test password'
    options.smtp_from = 'sender@example.com'
    options.blacklist_domains = ['bad.domain.com', 'another.bad.domain.com']
    return options


@patch('accounts.utils.logging')
@patch('accounts.utils.smtplib.SMTP')
def test_smtp_sendmail_no_smtp_details(SMTP, logging):
    host = ''
    port = 123
    user = ''
    password = ''
    send_from = ''

    accounts.utils.smtp_sendmail(host, port, user, password, send_from, '', None)

    assert not SMTP.called
    logging.warn.assert_called_once_with('SMTP Server not configured. Service will not be able '
                                         'to send emails until this is done.')


@patch('accounts.utils.logging')
@patch('accounts.utils.smtplib.SMTP')
def test_smtp_sendmail_invalid_smtp_details(SMTP, logging):
    host = 'invalid'
    port = 123
    user = 'invalid'
    password = 'invalid'
    send_from = 'invalid'

    SMTP.side_effect = smtplib.SMTPException
    accounts.utils.smtp_sendmail(host, port, user, password, send_from, '', None)

    SMTP.call_count == 1
    logging.warn.assert_called_once_with('Email could not be sent', exc_info=True)


@patch('accounts.utils.smtplib.SMTP')
def test_smtp_sendmail_valid(SMTP):
    host = 'test host'
    port = 123
    user = 'test user'
    password = 'test password'
    send_from = 'sender@example.com'

    smtpserver = SMTP.return_value

    accounts.utils.smtp_sendmail(host, port, user,
        password, send_from, 'test@example.com', 'test message')

    SMTP.assert_called_once_with('test host', 123)
    smtpserver.login.assert_called_once_with('test user', 'test password')
    smtpserver.sendmail.assert_called_once_with('sender@example.com', 'test@example.com', 'test message')
    smtpserver.quit.call_count == 1


@patch('accounts.utils.options')
@patch('accounts.utils.smtp_sendmail')
def test_send_email_single_recipient(smtp_sendmail, options):
    options = add_options(options)

    func = partial(accounts.utils.send_email, 'test@example.com', 'test subject', 'test message')
    IOLoop.instance().run_sync(func)

    assert smtp_sendmail.called
    args, kwargs = smtp_sendmail.call_args
    host = args[0]
    port = args[1]
    user = args[2]
    password = args[3]
    send_from = args[4]
    send_to = args[5]
    message = args[6]
    assert host == 'test host'
    assert port == 123
    assert user == 'test user'
    assert password == 'test password'
    assert send_from == 'sender@example.com'
    assert send_to == ['test@example.com']


@patch('accounts.utils.options')
@patch('accounts.utils.smtp_sendmail')
def test_send_email_multiple_recipients(smtp_sendmail, options):
    options = add_options(options)

    func = partial(accounts.utils.send_email, ['test1@example.com', 'test2@example.com'], 'test subject', 'test message')
    IOLoop.instance().run_sync(func)

    assert smtp_sendmail.called
    args, kwargs = smtp_sendmail.call_args
    host = args[0]
    port = args[1]
    user = args[2]
    password = args[3]
    send_from = args[4]
    send_to = args[5]
    message = args[6]
    assert host == 'test host'
    assert port == 123
    assert user == 'test user'
    assert password == 'test password'
    assert send_from == 'sender@example.com'
    assert send_to == ['test1@example.com', 'test2@example.com']


@patch('accounts.utils.options')
@patch('accounts.utils.smtp_sendmail')
def test_send_email_single_blacklisted_domain(smtp_sendmail, options):
    options = add_options(options)

    func = partial(accounts.utils.send_email, 'someone@bad.domain.com', 'test subject', 'test message')
    IOLoop.instance().run_sync(func)

    assert not smtp_sendmail.called


@patch('accounts.utils.options')
@patch('accounts.utils.smtp_sendmail')
def test_send_email_multiple_blacklisted_recipients(smtp_sendmail, options):
    options = add_options(options)

    send_addresses = ['keeper@example.com', 'someone@bad.domain.com', 'someone@another.bad.domain.com']

    func = partial(accounts.utils.send_email, send_addresses, 'test subject', 'test message')
    IOLoop.instance().run_sync(func)

    assert smtp_sendmail.called
    args, kwargs = smtp_sendmail.call_args
    host = args[0]
    port = args[1]
    user = args[2]
    password = args[3]
    send_from = args[4]
    send_to = args[5]
    message = args[6]
    assert host == 'test host'
    assert port == 123
    assert user == 'test user'
    assert password == 'test password'
    assert send_from == 'sender@example.com'
    assert send_to == ['keeper@example.com']


@patch('accounts.utils.options')
def test_build_mime_text_single_recipient(options):
    options = add_options(options)

    func = partial(accounts.utils.build_mime_text, ['test@example.com'], 'test subject', 'test message')
    result = IOLoop.instance().run_sync(func)

    assert result['Subject'] == 'test subject'
    assert result['From'] == 'sender@example.com'
    assert result['To'] == 'test@example.com'


@patch('accounts.utils.options')
def test_build_mime_text_multiple_recipients(options):
    options = add_options(options)

    func = partial(accounts.utils.build_mime_text, ['test1@example.com', 'test2@example.com'], 'test subject', 'test message')
    result = IOLoop.instance().run_sync(func)

    assert result['Subject'] == 'test subject'
    assert result['From'] == 'sender@example.com'
    assert result['To'] == 'test1@example.com,test2@example.com'


@patch('accounts.utils.options')
def test_build_mime_text_plain_text(options):
    options = add_options(options)

    func = partial(accounts.utils.build_mime_text, ['test@example.com'], 'test subject', 'test message')
    result = IOLoop.instance().run_sync(func)

    text = result.get_payload(0)
    html = result.get_payload(1)

    assert text.get_payload() == 'test message\n\n'
    assert text.get_content_type() == 'text/plain'
    assert html.get_payload() == 'test message'
    assert html.get_content_type() == 'text/html'


@patch('accounts.utils.options')
def test_build_mime_text_html_message(options):
    options = add_options(options)

    message = """<html>
                    <head></head>
                    <body>
                        <p>Hi!<br>
                           How are you?<br>
                           Here is the <a href="https://www.python.org">link</a> you wanted.
                        </p>
                    </body>
                 </html>
              """
    plain_text_message = "Hi!\n\nHow are you?\n\nHere is the [link][1] you wanted.\n\n   [1]: https://www.python.org\n\n"

    func = partial(accounts.utils.build_mime_text, ['test@example.com'], 'test subject', message)
    result = IOLoop.instance().run_sync(func)

    text = result.get_payload(0)
    html = result.get_payload(1)

    assert text.get_payload() == plain_text_message
    assert text.get_content_type() == 'text/plain'
    assert html.get_payload() == message
    assert html.get_content_type() == 'text/html'
