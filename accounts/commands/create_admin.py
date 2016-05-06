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
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301 USA
"""Create an admin user"""
from functools import partial

import click
import perch
from koi import load_config
from tornado.ioloop import IOLoop
from tornado.options import options

from accounts.app import CONF_DIR


@click.command(help='Create an admin user')
@click.argument('email')
@click.argument('password')
def cli(email, password):
    options.logging = None
    load_config(CONF_DIR)

    func = partial(perch.User.create_admin, email, password)
    user = IOLoop.instance().run_sync(func)

    return user
