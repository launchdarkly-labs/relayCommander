"""Relay Commander CLI
"""
import os
import subprocess
import sys

import click

from relay_commander.generators import ConfigGenerator
from relay_commander.ld import LaunchDarklyApi
from relay_commander.redis import updateRelay
from relay_commander.validator import validateState

@click.group()
def cli():
    pass

# @click.command()
# def deploy_relay():
#     """Deploy LD Relay to a VM."""
#     l = LaunchDarklyApi(os.environ.get('LD_API_KEY'), 'ldsolutions.tk')
#     envs = l.getEnvironments('support-service')
#     c = ConfigGenerator()

#     c.generate_relay_config(envs)

#     subprocess.run(
#         ["./scripts/deploy_relay.sh"]
#     )

@click.command()
def hello():
    click.echo("Hello World")

@click.command()
@click.option('-p', '--project', required=True)
@click.option('-e', '--environment', required=True)
@click.option('-f', '--feature', required=True)
@click.option('-s', '--state', required=True)
def update(project, environment, feature, state):
    ld = LaunchDarklyApi(os.environ.get('LD_API_KEY'), project, environment, feature)

    # # click.echo(l.getFlagStatus(project, environment))

    if validateState(state):
        validState = False if (state.lower() == 'false') else True
        r = updateRelay(ld, validState)
        click.echo(feature + " was successfully updated")
    else:
        print("Invalid state: " + state + ", -s needs to be either true or false")
    
    # # update LD API and poll for update

    #click.echo(ld.getFlagStatus(project, environment, feature))
    # click.echo('Project: ' + project + '; Environment: ' +
    #     environment + '; Flag_key: ' + flag_key)

cli.add_command(hello)
cli.add_command(update)

if __name__ == '__main__':
    cli()
