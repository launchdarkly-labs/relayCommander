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
        """Generate docker-compose.relay.yml."""
        template = self.env.get_template('docker-compose.relay.jinja')

        with open('docker-compose.relay.yml', 'w') as docker_compose_file:
            t = template.render(
                envs=environments
            )
            docker_compose_file.write(t)
