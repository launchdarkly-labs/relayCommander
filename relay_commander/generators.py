"""Generator Module.

Generates templates using jinja.
"""
from jinja2 import Environment, PackageLoader


class ConfigGenerator():
    """Abstract configuration generator using Jinja"""

    def __init__(self):
        self.env = Environment(
            loader=PackageLoader('relay_commander', 'templates')
        )

    def generate_relay_config(self, environments):
        """Generate ld-relay.conf file."""
        template = self.env.get_template('ld-relay.conf.jinja')

        with open('ld-relay.conf', 'w') as ldRelayFile:
            t = template.render(
                envs=environments
            )
            ldRelayFile.write(t)
