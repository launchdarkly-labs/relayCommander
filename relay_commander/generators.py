# -*- coding: utf-8 -*-
"""
relay_commander.generators
~~~~~~~~~~~~~~~~~~~~~~~~~~

This module allows for generating LaunchDarkly relay configurations
using Jinja templates.
"""
from jinja2 import Environment, PackageLoader


class ConfigGenerator():
    """Abstract configuration generator using Jinja."""

    def __init__(self):
        self.env = Environment(
            loader=PackageLoader('relay_commander', 'templates')
        )

    def generate_relay_config(self, environments: list) -> None:
        """Generate ld-relay.conf file.

        Given a list of environments of a project, this will generate a
        ``ld-relay.conf`` file in the current working directory. The conf file
        follows the specification that is documented in the main `ld-relay`_
        documentation.

        .. _ld-relay: https://github.com/launchdarkly/ld-relay#configuration-file-format

        :param environments: list of LaunchDarkly environments.
        """
        template = self.env.get_template('ld-relay.conf.jinja')

        with open('ld-relay.conf', 'w') as ldRelayFile:
            t = template.render(
                envs=environments
            )
            ldRelayFile.write(t)
