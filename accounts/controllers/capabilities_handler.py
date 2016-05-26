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

"""API Capabilities handler.
Return basic information about the service capabilities.
"""
import tornado.web
from tornado.options import options


class CapabilitiesHandler(tornado.web.RequestHandler):
    """Responsible for providing basic service capabilities, like:
    min/max acceptable registered service name, location etc.
    """

    def get(self):
        """Respond with JSON containing a list of not sensitive service
        capabilities.
        """
        capabilities = {k: options[k] for k
                        in options.non_sensitive_capabilities}

        self.finish({
            'status':200,
            'data': capabilities
        })
