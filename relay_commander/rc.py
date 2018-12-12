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

    if validateState(state):
        validState = False if (state.lower() == 'false') else True
        createFile(project, environment, feature, state)
        click.echo(feature + " was successfully updated")
    else:
        print("Invalid state: " + state + ", -s needs to be either true or false")

@click.command()
def playback():
    executeReplay()
    click.echo("LaunchDarkly is now update to date")


@click.command()
@click.option('-p', '--project', required=True)
@click.option('-e', '--environment', required=True)
@click.option('-f', '--feature', required=True)
@click.option('-s', '--state', required=True)
def ld_api(project, environment, feature, state):
    ld = LaunchDarklyApi(os.environ.get('LD_API_KEY'), project, environment, feature)

    if validateState(state):
        validState = False if (state.lower() == 'false') else True
        r = ld.updateFlag(validState)
    else:
        print("Invalid state: " + state + ", -s needs to be either true or false")

cli.add_command(hello)
cli.add_command(update)
cli.add_command(playback)
cli.add_command(ld_api)

if __name__ == '__main__':
    cli()
