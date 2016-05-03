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
from .base import BaseHandler


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

        yield email.send_create_request_emails(self.user, organisation)

        self.finish({'status': 200, 'data': organisation.clean()})

    @auth.auth_required(perch.Token.valid)
    @gen.coroutine
    def get(self):
        """Get all organisations"""
        state = self.get_argument('state', None)

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
        data = self.get_json_body(required=['asset_id', 'asset_id_type'])
        asset_id = data['asset_id']
        asset_id_type = data['asset_id_type']

        organisation = yield perch.Organisation.get(organisation_id)
        links = getattr(organisation, 'reference_links', {})

        result = {k: v.format(asset_id=asset_id) for k, v in links.items()
                  if k == asset_id_type}

        self.finish({
            'status': 200,
            'data': result
        })
