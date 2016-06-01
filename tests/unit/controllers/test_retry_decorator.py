# # -*- coding: utf-8 -*-
# # Copyright 2016 Open Permissions Platform Coalition
# # Licensed under the Apache License, Version 2.0 (the "License");
# # you may not use this file except in compliance with the License. You may obtain a copy of the License at
# # http://www.apache.org/licenses/LICENSE-2.0
# # Unless required by applicable law or agreed to in writing, software distributed under the License is
# # distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# # See the License for the specific language governing permissions and limitations under the License.
# #
#
import couch
from mock import Mock, patch
from tornado.web import Application
from tornado import testing

from accounts.controllers.base import BaseHandler, retry
from tornado.httpclient import HTTPError
from koi.test_helpers import make_future


class RetryMethodDecoratorWithRetries(testing.AsyncHTTPTestCase):
    def get_app(self):
        return Application([('/', self.Handler)])

    def setUp(self):
        self.get_method = Mock(side_effect=[couch.Conflict(HTTPError(409, 'Conflict')), make_future(None)])
        self.get_method.__name__ = 'get'

        class Handler(BaseHandler):
            pass

        setattr(Handler, 'get', retry(couch.Conflict)(self.get_method))
        self.Handler = Handler

        super(RetryMethodDecoratorWithRetries, self).setUp()

    @patch('accounts.controllers.base.options')
    def test(self, options):
        options.max_retries = 3

        self.fetch('/')
        assert self.get_method.call_count == 2


class RetryMethodDecoratorMaxRetries(testing.AsyncHTTPTestCase):
    def get_app(self):
        return Application([('/', self.Handler)])

    def setUp(self):
        self.get_method = Mock(side_effect=couch.Conflict(HTTPError(409, 'Conflict')))
        self.get_method.__name__ = 'get'

        class Handler(BaseHandler):
            pass

        setattr(Handler, 'get', retry(couch.Conflict)(self.get_method))
        self.Handler = Handler

        super(RetryMethodDecoratorMaxRetries, self).setUp()

    @patch('accounts.controllers.base.options')
    def test(self, options):
        options.max_retries = 3

        self.fetch('/')
        assert self.get_method.call_count == options.max_retries + 1


class RetryMethodDecoratorWithoutRetries(testing.AsyncHTTPTestCase):
    def get_app(self):
        return Application([('/', self.Handler)])

    def setUp(self):
        self.get_method = Mock(return_value=make_future(None))
        self.get_method.__name__ = 'get'

        class Handler(BaseHandler):
            pass

        setattr(Handler, 'get', retry(couch.Conflict)(self.get_method))
        self.Handler = Handler

        super(RetryMethodDecoratorWithoutRetries, self).setUp()

    @patch('accounts.controllers.base.options')
    def test(self, options):
        options.max_retries = 3

        self.fetch('/')
        assert self.get_method.call_count == 1

