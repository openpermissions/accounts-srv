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
