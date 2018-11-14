"""Relay Commander CLI
"""
import os
import subprocess
import sys

import click

from relay_commander.generators import ConfigGenerator
from relay_commander.ld import LaunchDarklyApi

@click.group()
def cli():
    pass

@click.command()
def deploy_relay():
    """Deploy LD Relay to a VM."""
    l = LaunchDarklyApi(os.environ.get('LD_API_KEY'), 'ldsolutions.tk')
    envs = l.getEnvironments('support-service')
    c = ConfigGenerator()

    c.generate_relay_config(envs)

    subprocess.run(
        ["./scripts/deploy_relay.sh"]
    )

@click.command()
def hello():
    click.echo("Hello World")

cli.add_command(deploy_relay)
cli.add_command(hello)

if __name__ == '__main__':
    cli()
