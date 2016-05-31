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

"""API Services handler. Allows to create and modify CH Service accounts"""
import couch
from koi import auth
from koi.exceptions import HTTPError
import perch
from perch.model import State
from perch.organisation import SERVICE_TYPES
from tornado.gen import coroutine

from accounts.models import email
from .base import BaseHandler, retry
from accounts.audit import audit_log


class ServiceTypes(BaseHandler):
    def get(self):
        self.finish({
            'status': 200,
            'data': sorted(list(SERVICE_TYPES))
        })


class Service(BaseHandler):

    @coroutine
    def get(self, service_id):
        """Get a service"""
        result = yield perch.Service.get(service_id)
        self.finish({
            'status': 200,
            'data': result.clean(user=self.user)
        })

    @auth.auth_required(perch.Token.valid)
    @coroutine
    def put(self, service_id):
        """Update a service"""
        data = self.get_json_body()

        service = yield perch.Service.get(service_id)
        yield service.update(self.user, **data)

        msg = ("updated service, service id: {}, data: {}"
               .format(service_id, data))
        audit_log.info(self, msg)

        if 'state' in data:
            creator = yield perch.User.get(service.created_by)
            yield email.send_request_update_email(
                creator,
                service,
                service.state,
                self.user,
                'create')

        self.finish({
            'status': 200,
            'data': service.clean(user=self.user)
        })

    @auth.auth_required(perch.Token.valid)
    @coroutine
    def delete(self, service_id):
        """Delete a service"""
        service = yield perch.Service.get(service_id)
        yield service.update(self.user, state=State.deactivated.name)

        audit_log.info(self, "deactivated service, service id: {}".format(service_id))

        self.finish({
            'status': 200,
            'data': {
                'message': 'service deactivated'
            }
        })


class ServicesHandler(BaseHandler):
    """Responsible for services"""

    @coroutine
    def get(self):
        """Get services"""
        organisation_id = self.get_argument('organisation_id', None)
        service_type = self.get_argument('type', None)

        if organisation_id:
            # check exists
            yield perch.Organisation.get(organisation_id)

        result = yield perch.Service.all(service_type, organisation_id)
        self.finish({
            'status': 200,
            'data': [x.clean(user=self.user) for x in result]
        })


class OrgServicesHandler(BaseHandler):
    """Responsible for an organisation's services"""

    @retry(couch.Conflict)
    @auth.auth_required(perch.Token.valid)
    @coroutine
    def post(self, organisation_id):
        """Create a service.
        At this stage a basic data validation is applied. Service Model is
        responsible for more detailed validation.
        It will:
        * on success: return a service object containing id and rev
        * on validation failure: return an errors object
        * on saving to DB: raise an CouchDB exception
        """
        if not self.user.is_user(organisation_id):
            raise HTTPError(403, 'Forbidden')

        data = self.get_json_body(required=['name', 'location', 'service_type'])
        data['created_by'] = self.user.id
        data['organisation_id'] = organisation_id

        service = yield perch.Service.create(user=self.user, **data)

        msg = ("created service, organisation id: {}, service_id: {}, data: {}"
               .format(organisation_id, service.id, data))
        audit_log.info(self, msg)

        if service.state == State.pending:
            yield email.send_create_request_emails(self.user, service)

        self.finish({
            'status': 200,
            'data': service.clean(user=self.user)
        })
