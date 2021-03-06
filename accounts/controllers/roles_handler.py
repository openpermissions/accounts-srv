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

"""API Roles handler. Allows to create and modify roles
"""
from koi import auth
from perch import Token, User
from tornado.gen import coroutine

from .base import BaseHandler


class RolesHandler(BaseHandler):
    """Responsible for managing role resources
    """

    @auth.auth_required(Token.valid)
    @coroutine
    def get(self):
        """Get all roles"""
        roles = {x.value for x in User.roles}
        result = [{'id': x, 'name': x.title()} for x in roles]

        self.finish({
            'status': 200,
            'data': result
        })
