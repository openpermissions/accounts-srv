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

"""API Organisations handler. Allows to create and modify organisation accounts
"""
from koi.base import BaseHandler
from perch.views import reference_links
from tornado import gen


class ReferenceLinks(BaseHandler):
    """Responsible for querying all reference links for all organisations"""
    @gen.coroutine
    def post(self):
        """Query for all organisations' reference links"""
        data = self.get_json_body(required=['asset_id', 'asset_id_type'])
        asset_id = data['asset_id']
        asset_id_type = data['asset_id_type']

        links = yield reference_links.get(key=asset_id_type)
        results = []

        for result in links['rows']:
            value = result['value']
            link = value['links'][asset_id_type].format(asset_id=asset_id)
            value['links'][asset_id_type] = link
            results.append(value)

        self.finish({
            'status': 200,
            'data': results
        })
