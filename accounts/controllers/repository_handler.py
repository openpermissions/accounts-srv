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
import couch
from tornado.gen import coroutine

from koi import auth
import perch
from perch.model import State

from ..models import email
from ..audit import audit_log
from .base import BaseHandler, retry


class OrganisationRepositories(BaseHandler):
    @coroutine
    def get(self, organisation_id):
        """Get repositories for an organisation"""
        organisation = yield perch.Organisation.get(organisation_id)

        repos = [perch.Repository(parent=organisation,
                                  organisation_id=organisation_id,
                                  id=repo_id,
                                  **repo)
                 for repo_id, repo in organisation.repositories.items() if repo['state'] != State.deactivated.name]

        repositories = yield [x.with_relations(user=self.user) for x in repos]

        self.finish({'status': 200, 'data': repositories})

    @retry(couch.Conflict)
    @auth.authorized(perch.Token.valid)
    @coroutine
    def post(self, organisation_id):
        """Create a repository for an organisation"""
        data = self.get_json_body(required=['name', 'service_id'])
        data['organisation_id'] = organisation_id
        data['created_by'] = self.user.id

        repository = yield perch.Repository.create(self.user, **data)

        msg = ("repository created, organisation_id:{}, "
               "repository id:{}, data:{}"
               .format(organisation_id, repository.id, data))
        audit_log.info(self, msg)

        if repository.state == State.pending:
            yield email.send_repository_request_emails(self.user, repository)

        result = yield repository.with_relations(user=self.user)

        self.finish({'status': 200, 'data': result})


class Repositories(BaseHandler):
    @coroutine
    def get(self):
        """Get repositories"""
        repositories = yield perch.Repository.all()
        result = yield [repo.with_relations(user=self.user) for repo in repositories]

        self.finish({
            'status': 200,
            'data': result
        })


class Respository(BaseHandler):
    @coroutine
    def get(self, repository_id):
        """Get a repository"""
        repo = yield perch.Repository.get(repository_id)
        result = yield repo.with_relations(user=self.user)
        self.finish({'status': 200, 'data': result})

    @retry(couch.Conflict)
    @auth.authorized(perch.Token.valid)
    @coroutine
    def delete(self, repository_id):
        """Delete a repository"""
        repository = yield perch.Repository.get(repository_id)
        yield repository.update(self.user, state=State.deactivated.name)

        audit_log.info(self, "deactivated repository, repository id: {}".format(repository_id))

        self.finish({
            'status': 200,
            'data': {
                'message': 'repository deactivated'
            }
        })

    @retry(couch.Conflict)
    @auth.authorized(perch.Token.valid)
    @coroutine
    def put(self, repository_id):
        """Update a repository"""
        data = self.get_json_body()
        repository = yield perch.Repository.get(repository_id)
        yield repository.update(self.user, **data)

        msg = ("repository updated, repository id:{}, data:{}"
               .format(repository_id, data))
        audit_log.info(self, msg)

        result = yield repository.with_relations(user=self.user)

        if 'state' in data:
            creator = yield perch.User.get(repository.created_by)
            yield email.send_request_update_email(
                creator,
                repository,
                repository.state,
                self.user,
                'create'
            )

        self.finish({'status': 200, 'data': result})
