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

"""API Users handler. Allows to create and modify user accounts
"""
import couch
from koi import auth
from .base import BaseHandler, retry
from koi.base import HTTPError
from tornado.gen import coroutine

import perch
from perch import exceptions
from perch.model import State
from accounts.models import email

from accounts.audit import audit_log

class UsersHandler(BaseHandler):
    """ Responsible for managing user resources """

    @auth.auth_optional(perch.Token.valid)
    @coroutine
    def post(self):
        """Create user"""
        data = self.get_json_body()
        try:
            password = data.pop('password')
        except KeyError:
            errors = [{
                'field': 'password',
                'message': 'user "password" is missing'
            }]

            # check for other validation errors
            try:
                yield perch.User(**data).validate()
            except exceptions.ValidationError as exc:
                errors.extend(exc.args[0])

            raise HTTPError(400, errors)

        try:
            user = yield perch.User.create(self.user, password, **data)
        except exceptions.ValidationError as exc:
            raise HTTPError(400, exc.args[0])

        audit_log.info(self, "user created, user_id: {}".format(user.id))

        # only send verification email if hash exists  
        if (getattr(user, 'verification_hash', None)) is not None: 
            audit_log.info(self, "send verification email to user_id: {}".format(user.id))
            yield email.send_verification_email(user)

        self.finish({
            'status': 200,
            'data': user.clean()
        })

    @auth.auth_required(perch.Token.valid)
    @coroutine
    def get(self):
        """Get all Users
        """
        users = yield perch.User.all()

        self.finish({
            'status': 200,
            'data': [user.clean() for user in users]
        })


class UserOrgsHandler(BaseHandler):
    """ Manages User-Organisations relationships, by adding an organisation_id """

    @auth.auth_required(perch.Token.valid)
    @coroutine
    def get(self, user_id):
        """ Gets all organisations associated with a user """
        state = self.get_argument('state', None)
        organisations = yield perch.Organisation.user_organisations(user_id, state)
        user = yield perch.User.get(user_id)
        user_orgs = getattr(user, 'organisations', {})

        result = [{
            'id': x.id,
            'name': x.name,
            'state': user_orgs.get(x.id, {}).get('state')
        } for x in organisations]

        self.finish({
            'status': 200,
            'data': result
        })

    @retry(couch.Conflict)
    @auth.auth_required(perch.Token.valid)
    @coroutine
    def post(self, user_id):
        """ Create User-Organisation relationship """
        data = self.get_json_body(required=['organisation_id'])
        organisation_id = data['organisation_id']
        pre_verified = data.get('pre_verified', False)

        try:
            organisation = yield perch.Organisation.get(organisation_id)
        except couch.NotFound:
            raise HTTPError(400, 'Organisation does not exist')

        if organisation.state != State.approved:
            raise HTTPError(400, 'Organisation is not approved')

        user_org = yield perch.UserOrganisation.create(
            user=self.user,
            id=organisation_id,
            user_id=user_id,
            pre_verified=pre_verified
        )

        user = user_org.parent

        msg = ("created user-organisation link, user id: {}, "
               "organisation id: {}".format(user_id, organisation_id))
        audit_log.info(self, msg)
        yield email.send_join_request_emails(user, organisation)

        self.finish({
            'status': 200,
            'data': user.clean()
        })


class UserOrgHandler(BaseHandler):
    """ Manages a User-Organisation relationship """

    @auth.auth_required(perch.Token.valid)
    @coroutine
    def get(self, user_id, organisation_id):
        """ Gets an organisation associated with a user """
        organisation = yield perch.Organisation.get(organisation_id)
        user_org = yield perch.UserOrganisation.get([user_id, organisation_id])

        self.finish({
            'status': 200,
            'data': {
                'id': organisation_id,
                'name': organisation.name,
                'role': user_org.role,
                'state': user_org.state.name
            }
        })

    @retry(couch.Conflict)
    @auth.auth_required(perch.Token.valid)
    @coroutine
    def put(self, user_id, organisation_id):
        """ Update the join state or role of a user's organisation """
        user_org = yield perch.UserOrganisation.get([user_id, organisation_id])

        body = self.get_json_body()
        if not ('state' in body or 'role' in body):
            raise HTTPError(400, 'state or role is required')

        yield user_org.update(self.user, **body)

        if 'state' in body:
            # Send email to user notifying of change in join state
            organisation = yield perch.Organisation.get(organisation_id)
            yield email.send_request_update_email(
                user_org.parent,
                organisation,
                body['state'],
                self.user,
                'join')

        self.finish({'status': 200, 'data': user_org.parent.clean()})

    @retry(couch.Conflict)
    @auth.auth_required(perch.Token.valid)
    @coroutine
    def delete(self, user_id, organisation_id):
        """ Delete a user's organisation """
        user_org = yield perch.UserOrganisation.get([user_id, organisation_id])
        yield user_org.update(self.user, state=State.deactivated.name)

        msg = ("deactivated user-organisation relation, user id: {}, "
               "organisation id: {}".format(user_id, organisation_id))
        audit_log.info(self, msg)

        self.finish({
            'status': 200,
            'data': user_org.parent.clean()
        })


class User(BaseHandler):
    """User resource"""

    @auth.auth_required(perch.Token.valid)
    @coroutine
    def get(self, user_id):
        """Get a user"""
        user = yield perch.User.get(user_id)

        self.finish({
            'status': 200,
            'data': user.clean()
        })

    @retry(couch.Conflict)
    @auth.auth_required(perch.Token.valid)
    @coroutine
    def put(self, user_id):
        """Update a user"""
        data = self.get_json_body()
        user = yield perch.User.get(user_id)
        try:
            yield user.update(self.user, **data)
        except exceptions.ValidationError as exc:
            raise HTTPError(400, exc.args[0])

        msg = "updated user, user id: {}, data: {}".format(user_id, data)
        audit_log.info(self, msg)

        self.finish({
            'status': 200,
            'data': user.clean()
        })

    @retry(couch.Conflict)
    @auth.auth_required(perch.Token.valid)
    @coroutine
    def delete(self, user_id):
        """Delete a user"""
        user = yield perch.User.get(user_id)
        yield user.update(self.user, state=State.deactivated.name)

        audit_log.info(self, "deactivated user, user id: {}".format(user_id))

        self.finish({
            'status': 200,
            'data': {'message': 'user deactivated'}
        })


class UserVerify(BaseHandler):
    @coroutine
    def put(self, user_id):
        """Verify a user based on verification hash"""
        body = self.get_json_body(required=['verification_hash'])
        try:
            user = yield perch.User.verify(user_id,
                                           body.get('verification_hash'))
        except exceptions.ValidationError as exc:
            raise HTTPError(400, exc.args[0])
        audit_log.info(self, "user verified, user id: {}".format(user_id))

        self.finish({
            'status': 200,
            'data': user.clean()
        })


class UserPassword(BaseHandler):
    @auth.auth_required(perch.Token.valid)
    @coroutine
    def put(self, user_id):
        """Change the user password"""
        body = self.get_json_body(required=['previous', 'password'])
        try:
            user = yield perch.User.get(user_id)
        except couch.NotFound:
            raise HTTPError(403, 'Forbidden')

        try:
            yield user.change_password(body['previous'], body['password'])
        except exceptions.Unauthorized:
            raise HTTPError(401, 'Unauthorized')

        audit_log.info(self, "user password changed, user id: {}".format(user_id))

        self.finish({
            'status': 200,
            'data': {
                'message': 'password changed'
            }
        })
