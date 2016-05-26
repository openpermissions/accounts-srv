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
