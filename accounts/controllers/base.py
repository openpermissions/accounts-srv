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

"base handler for accounts"
import couch
from tornado.gen import coroutine, Return
from koi import base
from perch import exceptions, Token, User


class BaseHandler(base.CorsHandler, base.JsonHandler):
    def send_error(self, status_code, **kwargs):
        exc = kwargs.get('exc_info', [None, None])[1]
        if isinstance(exc, couch.NotFound):
            self.set_status(404)
            self.write_error(404, reason=exc.args[1])
        elif isinstance(exc, exceptions.ValidationError):
            self.set_status(400)
            self.write_error(400, reason=exc.args[0])
        elif isinstance(exc, exceptions.Unauthorized):
            self.set_status(403)
            self.write_error(403, reason=exc.args[0])
        else:
            super(BaseHandler, self).send_error(status_code, **kwargs)

    @coroutine
    def is_authenticated(self, validator, *args, **kwargs):
        """
        verify if the request is authenticated
        :param validator: a validation function
        """
        if not self.token:
            raise Return(False)
        else:
            authenticated = yield validator(self.token, *args, **kwargs)
            raise Return(authenticated)

    @property
    def token(self):
        return self.request.headers.get('Authorization')

    @coroutine
    def prepare(self):
        self.user = None
        if self.token:
            try:
                token = yield Token.get(self.token)
                self.user = yield User.get(token.user_id)
            except couch.NotFound:
                # silently ignore invalid tokens
                pass
