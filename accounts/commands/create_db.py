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

"""
Create database
"""
import json

from tornado.options import options
import couch
import click
from koi import load_config

from accounts.app import CONF_DIR


def create_db(dbname, db_uri):
    """
    Create a database
    :param dbname: name of the database
    :param db_uri: uri of couch db
    """
    couchdb = couch.BlockingCouch(dbname, db_uri)
    list_of_dbs = couchdb.list_dbs()
    if dbname not in list_of_dbs:
        couchdb.create_db(db_name=dbname)
        print "Database '{}' created".format(dbname)
    else:
        print "Database '{}' already exists.  Not creating".format(dbname)


@click.command(help='create database')
@click.argument('dbname')
def cli(dbname):
    options.logging = None
    load_config(CONF_DIR)
    db_uri = '{}:{}'.format(
        options.url_registry_db, options.db_port)
    create_db(dbname, db_uri)
