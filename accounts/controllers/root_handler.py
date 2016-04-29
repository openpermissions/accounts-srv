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

"""API Root handler. Return basic information about the service.
"""
from koi import base


class RootHandler(base.BaseHandler):
    """Responsible for providing basic inf. on the service, like:
    + its name
    + current minor version
    """

    def initialize(self, **kwargs):
        try:
            self.version = kwargs['version']
        except KeyError:
            raise KeyError('version is required')

    def get(self):
        """Respond with JSON containing service name and current minor version
        of the service.
        """
        msg = {
            'status': 200,
            'data': {
                'service_name': 'Open Permissions Platform Accounts Service',
                'version': '{}'.format(self.version)
            }
        }

        self.finish(msg)
