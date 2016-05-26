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

"""Used to start the service from the parent directory using command:
    python accounts/
"""

import os
from accounts.app import main, CONF_DIR
from koi import commands

if __name__ == '__main__':
    commands_dir = os.path.join(os.path.dirname(__file__), 'commands')
    commands.cli(main, conf_dir=CONF_DIR, commands_dir=commands_dir)
