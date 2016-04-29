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

from __future__ import unicode_literals

from koi.test_helpers import gen_test, make_future
from mock import patch, mock_open, call
from perch import Organisation, Repository, User
from perch.model import State

from accounts.models import email


ADMINS = [
    'a@b.test',
    'c@d.test',
]
ADMIN = User(_id='admin1', name='admin user', email='mail@admin.test')
USER = User(
    first_name='test first',
    last_name='test last',
    verification_hash='testhash',
    password=User.hash_password('password0'),
    has_agreed_to_terms=True,
    email='test@example.com',
    _id='test id'
)
ORGANISATION = Organisation(
    _id='org1',
    name='test organisation'
)
REPOSITORY = Repository(
    id='repo1',
    organisation_id=ORGANISATION.id,
    name='test repo'
)


def setup_module():
    admins_patch = patch('accounts.models.email.views.admin_emails.values',
                         return_value=make_future(ADMINS))
    admins_patch.start()


def teardown_module():
    patch.stopall()


@patch('accounts.utils.send_email', return_value=make_future(True))
@gen_test
def test_send_verification_email(send_email):
    subject = 'Please verify your email address'

    fopen = mock_open(read_data='foo')
    with patch('__builtin__.open', fopen):
        yield email.send_verification_email(USER)

    fopen.assert_called_once_with(email.VERIFICATION_EMAIL_PATH)
    send_email.assert_called_once_with('test@example.com', subject, 'foo')


@patch('accounts.utils.send_email', return_value=make_future(True))
@gen_test
def test_send_verification_email_without_optional_user_params(send_email):
    user = User(
        verification_hash=USER.verification_hash,
        email=USER.email,
        password=USER.password,
        _id='test id',
        has_agreed_to_terms=USER.has_agreed_to_terms
    )
    subject = 'Please verify your email address'

    fopen = mock_open(read_data='foo')
    with patch('__builtin__.open', fopen):
        yield email.send_verification_email(user)

    fopen.assert_called_once_with(email.VERIFICATION_EMAIL_PATH)
    send_email.assert_called_once_with('test@example.com', subject, 'foo')


@patch('accounts.utils.send_email', return_value=make_future(True))
@gen_test
def test_send_join_request_emails(send_email):
    fopen = mock_open(read_data='foo')
    with patch('__builtin__.open', fopen):
        yield email.send_join_request_emails(USER, ORGANISATION)

    expected_calls = [call(email.USER_REQUEST_EMAIL_PATH),
                      call(email.ADMIN_REQUEST_EMAIL_PATH)]
    fopen.assert_has_calls(expected_calls, any_order=True)

    send_email.assert_has_calls([
        call(USER.email, 'Join request confirmation', 'foo'),
        call(ADMINS, 'Join request notification', 'foo')])


@patch('accounts.models.email._send_request_emails', return_value=make_future(True))
@gen_test
def test_send_repository_request_emails(_send_request_emails):
    yield email.send_repository_request_emails(USER, REPOSITORY)

    _send_request_emails.assert_called_once_with(
        USER, REPOSITORY, 'create', 'repository', admins=ADMINS)


@patch('accounts.utils.send_email', return_value=make_future(True))
@gen_test
def test_send_create_request_emails(send_email):
    fopen = mock_open(read_data='foo')
    with patch('__builtin__.open', fopen):
        yield email.send_create_request_emails(USER, ORGANISATION)

    expected_calls = [
        call(email.USER_REQUEST_EMAIL_PATH),
        call(email.ADMIN_REQUEST_EMAIL_PATH)
    ]

    fopen.assert_has_calls(expected_calls, any_order=True)

    send_email.assert_has_calls([
        call(USER.email, 'Create request confirmation', 'foo'),
        call(ADMINS, 'Create request notification', 'foo')])


@patch('accounts.utils.send_email', return_value=make_future(True))
@gen_test
def test_send_request_update_email_approved(send_email):
    fopen = mock_open(read_data='foo')
    with patch('__builtin__.open', fopen):
        result = yield email.send_request_update_email(
            USER,
            ORGANISATION,
            State.approved.value,
            ADMIN,
            'join')

    assert result is True
    fopen.assert_called_once_with(email.REQUEST_APPROVED_EMAIL_PATH)
    send_email.assert_called_once_with(USER.email, 'Join request approved', 'foo')


@patch('accounts.utils.send_email', return_value=make_future(True))
@gen_test
def test_send_request_update_email_rejected(send_email):
    fopen = mock_open(read_data='foo')
    with patch('__builtin__.open', fopen):
        result = yield email.send_request_update_email(
            USER,
            ORGANISATION,
            State.rejected.value,
            ADMIN,
            'join'
        )

    assert result is True
    fopen.assert_called_once_with(email.REQUEST_REJECTED_EMAIL_PATH)
    send_email.assert_called_once_with(USER.email, 'Join request rejected', 'foo')


@patch('accounts.utils.send_email')
@gen_test
def test_send_request_update_email_invalid(send_email):
    fopen = mock_open(read_data='foo')
    with patch('__builtin__.open', fopen):
        result = yield email.send_request_update_email(
            USER,
            ORGANISATION,
            'bar',
            ADMIN,
            'join'
        )

    assert result is False
    assert not fopen.called
    assert not send_email.called
