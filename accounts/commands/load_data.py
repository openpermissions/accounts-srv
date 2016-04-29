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

"""
fixture loader
"""
import json

from tornado.options import options
import couch
import click
from koi import load_config

from accounts.app import CONF_DIR


def load_docs(dbname, docs, db_uri):
    """
    save documents to a given database
    :param dbname: name of the database
    :param docs: a list of dictionaries representing the documents
    :param db_uri: uri of couch db
    """
    couchdb = couch.BlockingCouch(dbname, db_uri)
    try:
        couchdb.save_docs(docs)
    except couch.CouchException as exc:
        # http status code CREATED
        if exc.code == 201:
            print '\tdocs already exist'
        else:
            raise
    else:
        print '\tdocs successfully loaded'


@click.command(help='load fixture data')
@click.argument('files', nargs=-1, type=click.File('rb'))
def cli(files):
    options.logging = None
    load_config(CONF_DIR)
    # why do we care separating the protocol base url and the port?
    db_uri = '{}:{}'.format(
        options.url_registry_db, options.db_port)
    for fixture in files:
        print 'loading fixture file {}'.format(fixture.name)
        for dbname, docs in json.load(fixture).iteritems():
            print '\tloading docs into database "{}"'.format(dbname)
            load_docs(dbname, docs, db_uri)
