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

"""API Secrets handler. Allows to get, create and delete Service client secret credentials"""
import couch
import perch
from perch.model import State
from koi import auth
from koi.exceptions import HTTPError
from tornado.gen import coroutine

from accounts.audit import audit_log
from .base import BaseHandler, retry


class SecretsHandler(BaseHandler):
    @auth.auth_required(perch.Token.valid)
    @coroutine
    def get(self, service_id):
        """Get service client secrets"""
        service = yield perch.Service.get(service_id)
        approved = service.state == State.approved

        if not (self.user.is_user(service.organisation_id) and approved):
            raise HTTPError(403, 'Forbidden')

        secrets = yield perch.OAuthSecret.client_secrets(service_id)

        self.finish({
            'status': 200,
            'data': [x.secret for x in secrets]
        })

    @auth.auth_required(perch.Token.valid)
    @coroutine
    def post(self, service_id):
        """Add new client secret for service"""
        secret = yield perch.OAuthSecret.create(self.user, client_id=service_id)

        msg = ("client secret for service created, service id: {}"
               .format(service_id))
        audit_log.info(self, msg)

        self.finish({
            'status': 200,
            'data': secret.id
        })

    @retry(couch.Conflict)
    @auth.auth_required(perch.Token.valid)
    @coroutine
    def delete(self, service_id):
        """Delete all service secret credentials"""
        yield perch.OAuthSecret.delete_all_secrets(self.user, service_id)

        audit_log.info(self, "all service secrets deleted, service id: {}".format(service_id))

        self.finish({
            'status': 200,
            'data': {
                'message': 'secrets deleted'
            }
        })


class Secret(BaseHandler):
    @retry(couch.Conflict)
    @auth.auth_required(perch.Token.valid)
    @coroutine
    def delete(self, service_id, secret):
        """Delete given client secret for service"""
        secret = yield perch.OAuthSecret.get(secret)
        yield secret.delete(self.user)

        audit_log.info(self, "secret for service deleted, service id: {}".format(service_id))

        self.finish({
            'status': 200,
            'data': {
                'message': 'secret deleted'
            }
        })
