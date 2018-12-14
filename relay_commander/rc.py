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
from relay_commander.replayBuilder import createFile, executeReplay

@click.group()
def cli():
    pass

@click.command(name='update-redis')
@click.option('-p', '--project', required=True)
@click.option('-e', '--environment', required=True)
@click.option('-f', '--feature', required=True)
@click.option('-s', '--state', required=True)
def updateRedis(project, environment, feature, state):
    ld = LaunchDarklyApi(os.environ.get('LD_API_KEY'), project, environment)

    if validateState(state):
        validState = False if (state.lower() == 'false') else True
        updateRelay(ld, state, feature)
        createFile(project, environment, feature, state)
        click.echo("{0} was successfully updated.".format(feature))
    else:
        click.echo("Invalid state: {0}, -s needs to be either true or false.".format(state))

@click.command()
def playback():
    executeReplay()
    click.echo("LaunchDarkly is now update to date")

@click.command(name='update-ld-api')
@click.option('-p', '--project', required=True)
@click.option('-e', '--environment', required=True)
@click.option('-f', '--feature', required=True)
@click.option('-s', '--state', required=True)
def updateLdApi(project, environment, feature, state):
    ld = LaunchDarklyApi(os.environ.get('LD_API_KEY'), project, environment)

    if validateState(state):
        validState = False if (state.lower() == 'false') else True
        ld.updateFlag(validState, feature)
    else:
        click.echo('Invalid state: {0}, -s needs to be either true or false.'.format(state))

cli.add_command(updateRedis)
cli.add_command(playback)
cli.add_command(updateLdApi)

if __name__ == '__main__':
    cli()
