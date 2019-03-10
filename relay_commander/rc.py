# -*- coding: utf-8 -*-
"""
relay_commander.rc
~~~~~~~~~~~~~~~~~~

This module defines the relayCommander CLI.
"""
import os

import click
import click_log

from relay_commander.generators import ConfigGenerator
from relay_commander.ld import LaunchDarklyApi
from relay_commander.redis import RedisWrapper
from relay_commander.replayBuilder import createFile, executeReplay
from relay_commander.util import log
from relay_commander.validator import valid_env_vars, valid_state
from relay_commander.version import VERSION

# set up logging
click_log.basic_config(log)


@click.group()
@click.version_option(version=VERSION, prog_name='rc')
@click.help_option()
@click_log.simple_verbosity_option()
def cli() -> None:
    """Container for all cli commmands.

    Runs valid_env_vars() before each command invocation to verify that
    required Environment Variables are set and are not empty.

    .. versionchanged:: 0.0.12
    Added environment variable check before executing any other command.
    """
    valid_env_vars()


@click.command()
@click.option('-p', '--project', required=True)
@click.option('-e', '--environment', required=True)
@click.option('-f', '--feature', required=True)
@click.option('-s', '--state', required=True)
def update_redis(project, environment, feature, state):
    hosts = RedisWrapper.connectionStringParser(os.environ.get('REDIS_HOSTS'))

    for host in hosts:
        log.info("connecting to {0}:{1}".format(host.host, host.port))
        try:
            if valid_state(state):
                newState = state.lower()
                r = RedisWrapper(
                    host.host,
                    host.port,
                    log,
                    project,
                    environment
                )
                r.updateFlagRecord(newState, feature)
                createFile(project, environment, feature, newState)
                log.info("{0} was successfully updated.".format(feature))
            else:
                raise Exception('Invalid state: {0}, -s needs \
                    to be either on or off.'.format(state))
        except Exception as ex:
            log.error("unable to update {0}. Exception: {1}".format(
                host.host,
                ex
            ))
            exit(1)


@click.command()
def playback():
    try:
        executeReplay(log)
    except Exception:
        log.error('Unable to Execute Replay.')
        exit(1)


@click.command(name='update-ld-api')
@click.option('-p', '--project', required=True)
@click.option('-e', '--environment', required=True)
@click.option('-f', '--feature', required=True)
@click.option('-s', '--state', required=True)
def updateLdApi(project, environment, feature, state):
    ld = LaunchDarklyApi(
        os.environ.get('LD_API_KEY'),
        project,
        environment,
        log
    )

    if valid_state(state):
        validState = False if (state.lower() == 'off') else True
        ld.updateFlag(validState, feature)
    else:
        raise Exception('Invalid state: {0}, -s needs to be either \
            on or off.'.format(state))
        exit(1)


@click.command(name='generate-relay-config')
@click.option('-p', '--project', required=True)
def generateRelayConfig(project):
    """Generate Relay Proxy Configuration

    Generate a ld-relay.conf file to quickly spin up a relay proxy.
    Right now this is mostly used for integration testing.

    :param project: LaunchDarkly project key
    """
    ld = LaunchDarklyApi(
        os.environ.get('LD_API_KEY'),
        projectKey=project,
        logger=log
    )
    config = ConfigGenerator()

    envs = ld.getEnvironments(project)
    config.generate_relay_config(envs)


cli.add_command(update_redis)
cli.add_command(playback)
cli.add_command(updateLdApi)
cli.add_command(generateRelayConfig)

if __name__ == '__main__':
    cli()
