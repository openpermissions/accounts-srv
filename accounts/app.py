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

"""Configures and starts up the Accounts Service.
"""
import logging
import os.path

import koi
from tornado.ioloop import IOLoop
from tornado.options import options, define

from . import __version__
from .controllers import (
    root_handler, capabilities_handler, secrets_handler, organisations_handler, users_handler,
    services_handler, login_handler, roles_handler,
    repository_handler, reference_links_handler)
from .audit import configure_logging

# directory containing the config files
CONF_DIR = os.path.join(os.path.dirname(__file__), '../config')


define("env", default="dev")

def prepare_config(options):
    if not (options.smtp_host and options.smtp_port and options.smtp_from and
            options.smtp_user and options.smtp_pass):
        logging.warn('SMTP Server not configured. '
                     'Service will not be able to send emails until this is done.')


APPLICATION_URLS = [
    (r"", root_handler.RootHandler, {'version': __version__}),
    (r"/capabilities", capabilities_handler.CapabilitiesHandler),
    (r"/login", login_handler.LoginHandler),
    (r"/users",  users_handler.UsersHandler),
    (r"/users/{user_id}", users_handler.User),
    (r"/users/{user_id}/roles", users_handler.UserRolesHandler),
    (r"/users/{user_id}/verify", users_handler.UserVerify),
    (r"/users/{user_id}/password", users_handler.UserPassword),
    (r"/users/{user_id}/organisations", users_handler.UserOrgsHandler),
    (r"/users/{user_id}/organisations/{organisation_id}", users_handler.UserOrgHandler),

    (r"/organisations", organisations_handler.OrganisationsHandler),
    (r"/organisations/{organisation_id}", organisations_handler.Organisation),
    (r"/organisations/{organisation_id}/services", services_handler.OrgServicesHandler),
    (r"/organisations/{organisation_id}/repositories", repository_handler.OrganisationRepositories),
    (r"/organisations/{organisation_id}/links", organisations_handler.OrganisationReferenceLinks),

    (r"/services", services_handler.ServicesHandler),
    (r"/services/types", services_handler.ServiceTypes),
    (r"/services/{service_id}", services_handler.Service),
    (r"/services/{service_id}/secrets", secrets_handler.SecretsHandler),
    (r"/services/{service_id}/secrets/{secret}", secrets_handler.Secret),

    (r"/repositories", repository_handler.Repositories),
    (r"/repositories/{repository_id}", repository_handler.Respository),

    (r"/roles", roles_handler.RolesHandler),

    (r"/links", reference_links_handler.ReferenceLinks),
]


def main():
    """
    The entry point for the Accounts service.
    This will load the configuration files and start a Tornado webservice
    with one or more sub processes.

    NOTES:
    tornado.options.parse_command_line(final=True)
    Allows you to run the service with custom options.

    Examples:
        Change the logging level to debug:
            + python accounts --logging=DEBUG
            + python accounts --logging=debug

        Configure custom syslog server:
            + python accounts --syslog_host=54.77.151.169
    """
    koi.load_config(CONF_DIR)
    app = koi.make_application(
        __version__,
        options.service_type,
        APPLICATION_URLS)

    configure_logging()
    server = koi.make_server(app)

    # Forks multiple sub-processes, one for each core
    server.start(int(options.processes))
    prepare_config(options)

    IOLoop.instance().start()


if __name__ == '__main__':      # pragma: no cover
    main()                      # pragma: no cover
