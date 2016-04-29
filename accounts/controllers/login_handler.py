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

"""API Authentication Token handler. Allows to create and validate tokens
"""
from perch.exceptions import Unauthorized
from perch import User
from koi.base import BaseHandler
from koi.exceptions import HTTPError
from tornado.gen import coroutine


class LoginHandler(BaseHandler):
    """Responsible for user login
    """

    @coroutine
    def post(self):
        """Create token"""
        # TODO: what if unverified user?
        data = self.get_json_body(required=['email', 'password'])
        try:
            user, token = yield User.login(data['email'], data['password'])
        except Unauthorized:
            raise HTTPError(401, 'Invalid email and/or password')

        self.finish({
            'status': 200,
            'data': {
                'token': token,
                'user': user.clean()
            }
        })
