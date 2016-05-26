# -*- coding: utf-8 -*-
# Copyright © 2014-2016 Digital Catapult and The Copyright Hub Foundation
# (together the Open Permissions Platform Coalition)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# 

"""Model for all email sending
"""
import os.path

from perch import views, Organisation
from perch.model import State
from tornado.gen import coroutine, Return

import accounts.utils

VERIFICATION_EMAIL_PATH = os.path.join(
    os.path.dirname(__file__),
    '../templates/email/verification_template.html')

USER_REQUEST_EMAIL_PATH = os.path.join(
    os.path.dirname(__file__),
    '../templates/email/user_request_template.html')

ADMIN_REQUEST_EMAIL_PATH = os.path.join(
    os.path.dirname(__file__),
    '../templates/email/admins_request_template.html')

REQUEST_APPROVED_EMAIL_PATH = os.path.join(
    os.path.dirname(__file__),
    '../templates/email/approved_request_template.html')

REQUEST_REJECTED_EMAIL_PATH = os.path.join(
    os.path.dirname(__file__),
    '../templates/email/rejected_request_template.html')


@coroutine
def send_verification_email(user):
    """
    Sends an email to user asking for verification

    :param user: perch User object
    """
    with open(VERIFICATION_EMAIL_PATH) as template:
        message = template.read().format(
            email=user.email,
            name=getattr(user, 'first_name', None),
            user_id=user.id,
            verification_hash=getattr(user, 'verification_hash', None)
        )

    yield accounts.utils.send_email(
        user.email,
        'Please verify your email address',
        message
    )
    raise Return(True)


@coroutine
def send_repository_request_emails(user, repository):
    """
    Sends an email to user and to owner of repository service notifying of repository request.

    :param user: the user
    :param repository: the repository that is the subject of the request
    """
    admins = yield views.admin_emails.values(key=repository.organisation_id)
    yield _send_request_emails(
        user,
        repository,
        'create',
        'repository',
        admins=admins)

    raise Return(True)


@coroutine
def send_create_request_emails(user, entity):
    """
    Sends an email to user and to system admins notifying of create request.

    :param user: the user
    :param entity: the organisation/service that is the subject of the request
    """
    if entity.resource_type == Organisation.resource_type:
        organisation_id = entity.id
    else:
        organisation_id = entity.organisation_id
    admins = yield views.admin_emails.values(key=organisation_id)

    yield _send_request_emails(
        user,
        entity,
        'create',
        entity.resource_type,
        admins=admins)
    raise Return(True)


@coroutine
def send_join_request_emails(user, organisation):
    """
    Sends an email to user and to org admins notifying of join request.

    :param user: the user make the request
    :param organisation: the organisation that is the subject of the request
    """
    admins = yield views.admin_emails.values(key=organisation.id)
    yield _send_request_emails(
        user,
        organisation,
        'join',
        'organisation',
        admins=admins)

    raise Return(True)


@coroutine
def send_request_update_email(user, entity, state, admin_user, request_type):
    """
    Sends an email to user notifying them of update to their request.

    :param user: the user
    :param entity: the entity that is subject of request
    :param state: state that the request has been set to
    :param admin_user: the user who has changed state
    :param request_type: the request type
    """
    if state == State.approved:
        result = yield _send_approval_email(user, entity, request_type)
    elif state == State.rejected:
        result = yield _send_rejection_email(
            user, entity, admin_user, request_type)
    else:
        result = False

    raise Return(result)


@coroutine
def _send_request_emails(user, organisation, request_type, entity_type, admins=None):
    """
    Sends email to user and to admins notifying of request.

    :param user: the user making the request
    :param organisation: the organisation that is the subject of the request
    :param request_type - the request type
    :param admins: list of admin email addresses
    """
    first_name = getattr(user, 'first_name', None)
    with open(USER_REQUEST_EMAIL_PATH) as template:
        message = template.read().format(
            email=user.email,
            name=first_name,
            organisation=organisation.name,
            request_type=request_type,
            entity_type=entity_type,
            entity_name=organisation.name)

    yield accounts.utils.send_email(
        user.email,
        request_type.capitalize() + ' request confirmation',
        message
    )

    if admins:
        with open(ADMIN_REQUEST_EMAIL_PATH) as template:
            message = template.read().format(
                name=first_name,
                organisation=organisation.name,
                request_type=request_type,
                entity_type=entity_type,
                entity_name=organisation.name)

        yield accounts.utils.send_email(
            admins,
            request_type.capitalize() + ' request notification',
            message
        )


@coroutine
def _send_approval_email(user, entity, request_type):
    """
    Sends an email to user notifying them that their join request
    was approved.

    :param user: user making the request
    :param entity: organisation/service obj the user reqeusts to join
    :param request_type: the request type
    """
    with open(REQUEST_APPROVED_EMAIL_PATH) as template:
        message = template.read().format(
            name=getattr(user, 'first_name', None),
            entity_name=entity.name,
            request_type=request_type,
            entity_type=entity.resource_type)
        subject = request_type.capitalize() + ' request approved'

    yield accounts.utils.send_email(user.email, subject, message)

    raise Return(True)


@coroutine
def _send_rejection_email(user, entity, admin_user, request_type):
    """
    Sends an email to user notifying them that their join request
    was approved.

    :param user: the user
    :param entity: entity the user requested to join
    :param admin_user: the user who has changed the state
    :param request_type: the request type
    """
    with open(REQUEST_REJECTED_EMAIL_PATH) as template:
        message = template.read().format(
            name=getattr(user, 'first_name', None),
            entity_name=entity.name,
            admin_email=admin_user.email,
            request_type=request_type,
            entity_type=entity.resource_type)
        subject = request_type.capitalize() + ' request rejected'

    yield accounts.utils.send_email(user.email, subject, message)

    raise Return(True)
