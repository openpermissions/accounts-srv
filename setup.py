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

from setuptools import find_packages, setup
import accounts

setup(
    name='open permissions platform accounts service',
    version=accounts.__version__,
    description='Open Permissions Platform Accounts Service',
    author='Open Permissions Platform Coalition',
    author_email='support-copyrighthub@cde.catapult.org.uk',
    url='https://github.com/openpermissions/accounts-srv',
    packages=find_packages(exclude=['test']),
    entry_points={
        'console_scripts':
        ['open-permissions-platform-accounts-svr = accounts.app:main']},
    )
