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
from relay_commander.dynamodb_wrapper import DdbWrapper
from relay_commander.replay_builder import create_file, execute_replay
from relay_commander.util import LOG
from relay_commander.validator import valid_ld_api_vars, valid_redis_vars,valid_state
from relay_commander.version import VERSION

# set up logging
click_log.basic_config(LOG)


@click.group()
@click_log.simple_verbosity_option()
@click.version_option(version=VERSION, prog_name='rc')
@click.help_option()
def cli() -> None:
    """
    A CLI for working with LaunchDarkly relay instances.
    """

@click.command()
@click.option('-d', '--datastore', required=True)
@click.option('-p', '--project', required=True)
@click.option('-e', '--environment', required=True)
@click.option('-f', '--feature', required=True)
@click.option('-s', '--state', required=True)
@click.option('-t', '--table', required=False)
def update(datastore: str, project: str, environment: str, feature: str, state: str, table: str) \
        -> None:
    """
    Update data store for a feature flag.

    :param datastore: Datastore used: either redis or dynamodb.
    :param project: LaunchDarkly project key.
    :param environment: LaunchDarkly environment key.
    :param feature: LaunchDarkly feature key.
    :param state: State for a feature flag.
    :param table: Table name for DynamoDB.
    """
    try:
        if datastore == "redis":
            update_redis(project, environment, feature, state)
        elif datastore == "dynamodb":
            if table:
                update_dynamodb(project, environment, feature, state, table)
            else:
                LOG.error("Table name must be specified for DynamoDB")
        else:
            LOG.error("Datastore needs to be either: redis or dynamodb")
    except RuntimeError as ex:
        LOG.error(ex)
        sys.exit(1)

def update_redis(project: str, environment: str, feature: str, state: str) \
        -> None:
    """
    Update redis state for a feature flag.

    :param project: LaunchDarkly project key.
    :param environment: LaunchDarkly environment key.
    :param feature: LaunchDarkly feature key.
    :param state: State for a feature flag.
    """
    valid_redis_vars()
    try:
        hosts = RedisWrapper.connection_string_parser(
            os.environ.get('REDIS_HOSTS'))
    except RuntimeError as ex:
        LOG.error(ex)
        sys.exit(1)

    for host in hosts:
        try:
            if valid_state(state):
                new_state = state.lower()
                redis = RedisWrapper(
                    host.host,
                    host.port,
                    project,
                    environment
                )
                LOG.info("connecting to %s:%s with redis key: %s", host.host, host.port, redis._format_key_name())
                redis.update_flag_record(new_state, feature)
                create_file(project, environment, feature, state)
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
    Execute commands in the replay/toDo directory.
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
    valid_ld_api_vars()
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
@click.option('-s', '--store', required=True)
def generate_relay_config(project, store):
    """
    Generate Relay Proxy Configuration.

    Generate a ld-relay.conf file to quickly spin up a relay proxy.
    Right now this is mostly used for integration testing.

    :param project: LaunchDarkly project key
    :param store: feature store, either dynamodb or redis
    """
    valid_ld_api_vars()
    ld_api = LaunchDarklyApi(
        os.environ.get('LD_API_KEY'),
        project_key=project
    )
    config = ConfigGenerator()
    envs = ld_api.get_environments(project)
    config.generate_relay_config(envs, store)

def update_dynamodb(project: str, environment: str, feature: str, state: str, table: str) \
-> None:
    """
    Update DynamoDB for a feature flag

    :param table: table name for DynamoDB.
    :param project_key: LaunchDarkly project key
    :param environment_key: LaunchDarkly environment key.
    :param feature: LaunchDarkly feature key.
    :param state: State for a feature flag.

    """
    try:
        ddb = DdbWrapper(table, project, environment)
        LOG.info("connecting to DynamoDB table: %s with namespace: %s", table, ddb._format_namespace())
    except RuntimeError as ex:
        LOG.error(ex)
        sys.exit(1)

    if valid_state(state):
        new_state = state.lower()
        ddb.update_ddb_flag_record(feature, new_state)
        create_file(project, environment, feature, state)
        LOG.info("%s was successfully updated.", feature)
    else:
        LOG.error('Invalid state: {0}, -s needs to be either on or off.'.format(state))

cli.add_command(update)
cli.add_command(playback)
cli.add_command(update_ld_api)
cli.add_command(generate_relay_config)

if __name__ == '__main__':
    cli()
