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

from functools import wraps
import logging
from tornado.options import options
from koi.configure import log_formatter

AUDIT_LOG = 'opp.audit'
_audit_log = logging.getLogger(AUDIT_LOG)
_audit_log_enabled = False


def configure_logging():
    global _audit_log_enabled
    _audit_log_enabled = True
    _audit_log.setLevel(logging.INFO)
    handler = logging.handlers.TimedRotatingFileHandler(
        filename=getattr(options, 'audit_log_file_prefix', 'audit.log'),
        when='midnight',
        backupCount=10)
    handler.setFormatter(log_formatter())
    _audit_log.addHandler(handler)


def request_info(handler):
    if not getattr(handler, 'user', None):
        return "user: anonymous - "
    else:
        return "user: {user_id} - ".format(user_id=handler.user.id)


def with_handler_info(func):
    @wraps(func)
    def wrapper(handler, arg0, *args, **kwargs):
        if _audit_log_enabled:
            if handler is not None:
                pref = request_info(handler)
            else:
                pref = ""
            return func(pref + arg0, *args, **kwargs)

    return wrapper


class audit_log:
    info = staticmethod(with_handler_info(_audit_log.info))
    warning = staticmethod(with_handler_info(_audit_log.warning))
    error = staticmethod(with_handler_info(_audit_log.error))
    debug = staticmethod(with_handler_info(_audit_log.debug))
    exception = staticmethod(with_handler_info(_audit_log.exception))
