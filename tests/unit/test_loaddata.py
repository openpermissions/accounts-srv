# -*- coding: utf-8 -*-
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

import os

import pytest
from mock import MagicMock, patch
import couch

from accounts.commands.load_data import cli, load_docs


FIXTURE_DIR = os.path.join(os.path.dirname(__file__), '..', '..', 'fixtures')


@patch('accounts.commands.load_data.couch.BlockingCouch')
def test_save_docs(BlockingCouch):
    load_docs('db', [{'foo': 'bar'}], 'db_uri')


@patch('accounts.commands.load_data.couch.BlockingCouch')
def test_save_docs_already_exists(BlockingCouch):
    BlockingCouch().save_docs.side_effect = couch.CouchException(
        MagicMock(code=201))
    load_docs('db', [{'foo': 'bar'}], 'db_uri')


@patch('accounts.commands.load_data.couch.BlockingCouch')
def test_save_docs_other_error_code(BlockingCouch):
    BlockingCouch().save_docs.side_effect = couch.CouchException(
        MagicMock(code=202))
    with pytest.raises(couch.CouchException):
        load_docs('db', [{'foo': 'bar'}], 'db_uri')


@patch('accounts.commands.load_data.load_config')
@patch('accounts.commands.load_data.options')
@patch('accounts.commands.load_data.load_docs')
def test_cli(load_docs, options, _):
    with pytest.raises(SystemExit) as exc:
        cli([os.path.abspath(os.path.join(FIXTURE_DIR, 'user.json'))])

    assert exc.value.code == 0
