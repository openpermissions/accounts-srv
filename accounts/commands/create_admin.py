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

"""Create an admin user"""
from functools import partial
import socket

import click
import perch
from perch.exceptions import ValidationError
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
    try:
        IOLoop.instance().run_sync(func)
    except ValidationError as exc:
        raise click.ClickException(exc.args[0])
    except socket.error:
        raise click.ClickException('Unable to connect to CouchDB')
