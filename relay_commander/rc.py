# -*- coding: utf-8 -*-
"""
relay_commander.rc
~~~~~~~~~~~~~~~~~~

This module defines the relayCommander CLI using the click library.
"""
import os
import sys

import click
import click_log

from relay_commander.generators import ConfigGenerator
from relay_commander.ld import LaunchDarklyApi
from relay_commander.redis_wrapper import RedisWrapper
from relay_commander.replay_builder import create_file, execute_replay
from relay_commander.util import LOG
from relay_commander.validator import valid_env_vars, valid_state
from relay_commander.version import VERSION

# set up logging
click_log.basic_config(LOG)


@click.group()
@click.version_option(version=VERSION, prog_name='rc')
@click.help_option()
@click_log.simple_verbosity_option()
def cli() -> None:
    """
    Container for all cli commmands.

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
def update_redis(project: str, environment: str, feature: str, state: str) \
        -> None:
    """
    Update redis state for a feature flag.

    :param project: LaunchDarkly project key.
    :param environment: LaunchDarkly environment key.
    :param feature: LaunchDarkly feature key.
    :param state: State for a feature flag.
    """
    try:
        hosts = RedisWrapper.connection_string_parser(
            os.environ.get('REDIS_HOSTS'))
    except RuntimeError as ex:
        LOG.error(ex)
        sys.exit(1)

    for host in hosts:
        LOG.info("connecting to %s:%s", host.host, host.port)
        try:
            if valid_state(state):
                new_state = state.lower()
                redis = RedisWrapper(
                    host.host,
                    host.port,
                    project,
                    environment
                )
                redis.update_flag_record(new_state, feature)
                create_file(project, environment, feature, new_state)
                LOG.info("%s was successfully updated.", feature)
            else:
                raise Exception('Invalid state: {0}, -s needs \
                    to be either on or off.'.format(state))
        except KeyError as ex:
            LOG.error("unable to update %s. Exception: %s",
                      host.host,
                      ex)
            sys.exit(1)


@click.command()
def playback():
    """
    Attempt to play back all commands in the replay/toDo directory.
    """
    try:
        execute_replay()
    except ValueError as ex:
        LOG.error(ex)
        sys.exit(1)


@click.command()
@click.option('-p', '--project', required=True)
@click.option('-e', '--environment', required=True)
@click.option('-f', '--feature', required=True)
@click.option('-s', '--state', required=True)
def update_ld_api(project: str, environment: str, feature: str, state: str):
    """
    Execute command against the LaunchDarkly API.

    This command is generally not used directly, instead it is called as a
    part of running the ``playback()`` function.

    :param project: LaunchDarkly project key.
    :param environment: LaunchDarkly environment key.
    :param feature: LaunchDarkly feature key.
    :param state: State for a feature flag.
    """
    ld_api = LaunchDarklyApi(
        os.environ.get('LD_API_KEY'),
        project,
        environment
    )

    if valid_state(state):
        if state.lower() == 'off':
            new_state = False
        else:
            new_state = True
        ld_api.update_flag(new_state, feature)
    else:
        raise ValueError('Invalid state: {0}, -s needs to be either \
            on or off.'.format(state))


@click.command()
@click.option('-p', '--project', required=True)
def generate_relay_config(project):
    """Generate Relay Proxy Configuration

    Generate a ld-relay.conf file to quickly spin up a relay proxy.
    Right now this is mostly used for integration testing.

    :param project: LaunchDarkly project key
    """
    ld_api = LaunchDarklyApi(
        os.environ.get('LD_API_KEY'),
        project_key=project
    )
    config = ConfigGenerator()

    envs = ld_api.get_environments(project)
    config.generate_relay_config(envs)


cli.add_command(update_redis)
cli.add_command(playback)
cli.add_command(update_ld_api)
cli.add_command(generate_relay_config)

if __name__ == '__main__':
    cli()
