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

"""API Organisations handler. Allows to create and modify organisation accounts
"""
import couch
import perch
from perch import exceptions
from perch.model import State
from koi import auth
from koi.base import HTTPError
from tornado import gen

from accounts.models import email

from accounts.audit import audit_log
from .base import BaseHandler, retry


class Organisation(BaseHandler):
    @gen.coroutine
    def get(self, organisation_id):
        """Get an organisation"""
        try:
            result = yield perch.Organisation.get(organisation_id)
        except couch.NotFound:
            raise HTTPError(404, 'Not Found')

        self.finish({
            'status': 200,
            'data': result.clean()
        })

    @retry(couch.Conflict)
    @auth.auth_required(perch.Token.valid)
    @gen.coroutine
    def put(self, organisation_id):
        """Update an organisation"""
        data = self.get_json_body()
        try:
            organisation = yield perch.Organisation.get(organisation_id)
        except couch.NotFound:
            raise HTTPError(404, 'Not Found')

        yield organisation.update(self.user, **data)

        audit_log.info(self, "organisation updated, organisation_id:{}".format(organisation_id))

        if 'state' in data:
            creator = yield perch.User.get(organisation.created_by)
            yield email.send_request_update_email(
                creator,
                organisation,
                organisation.state,
                self.user,
                'create')

        self.finish({'status': 200, 'data': organisation.clean()})

    @retry(couch.Conflict)
    @auth.auth_required(perch.Token.valid)
    @gen.coroutine
    def delete(self, organisation_id):
        """Delete an organisation"""
        organisation = yield perch.Organisation.get(organisation_id)
        yield organisation.update(self.user, state=State.deactivated.name)
        yield perch.User.remove_organisation_from_all(organisation_id)

        audit_log.info(self, "organisation deactivated, organisation id:{}"
                       .format(organisation_id))

        self.finish({
            'status': 200,
            'data': {
                'message': 'organisation deactivated'
            }
        })


class OrganisationsHandler(BaseHandler):
    """Responsible for creating an organisation entity"""

    @auth.auth_required(perch.Token.valid)
    @gen.coroutine
    def post(self):
        """Create an organisation"""
        data = self.get_json_body()
        data['created_by'] = self.user.id

        try:
            organisation = yield perch.Organisation.create(self.user, **data)
        except exceptions.ValidationError as exc:
            raise HTTPError(400, exc.args[0])

        msg = ("organisation created, organisation id:{}, data: {}"
               .format(organisation.id, data))
        audit_log.info(self, msg)

        if not (self.user.is_reseller() and data.get('pre_verified', False)):
            yield email.send_create_request_emails(self.user, organisation)

        self.finish({'status': 200, 'data': organisation.clean()})

    @auth.auth_required(perch.Token.valid)
    @gen.coroutine
    def get(self):
        """Get all organisations, or filter by name if specified"""
        state = self.get_argument('state', None)

        name = self.get_query_argument('name', None)
        if name:
            result = yield perch.Organisation.get_by_name(searchName=name)
        else:
            try:
                result = yield perch.Organisation.all(state=state)
            except exceptions.ValidationError as exc:
                raise HTTPError(400, exc.args[0])

        self.finish({
            'status': 200,
            'data': [r.clean() for r in result]
        })


class OrganisationReferenceLinks(BaseHandler):
    @gen.coroutine
    def post(self, organisation_id):
        """Query for the reference links for an organisation"""
        data = self.get_json_body(required=['source_id', 'source_id_type'])
        source_id = data['source_id']
        source_id_type = data['source_id_type']

        organisation = yield perch.Organisation.get(organisation_id)
        reference_links = getattr(organisation, 'reference_links', {})
        links = reference_links.get('links', {})

        link = links.get(source_id_type)

        if not link:
            raise HTTPError(404, 'Not Found')

        self.finish({
            'status': 200,
            'data': link.format(source_id=source_id)
        })
