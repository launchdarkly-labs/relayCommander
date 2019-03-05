"""Relay Commander CLI
"""
import logging
import os

import click

import click_log
from relay_commander.generators import ConfigGenerator
from relay_commander.ld import LaunchDarklyApi
from relay_commander.redis import RedisWrapper
from relay_commander.replayBuilder import createFile, executeReplay
from relay_commander.validator import validateState

# set up logging
logger = logging.getLogger(__name__)
click_log.basic_config(logger)


@click.group()
@click.version_option(version='0.0.11', prog_name='relayCommander')
@click.help_option()
@click_log.simple_verbosity_option(logger)
def cli():
    pass


@click.command(name='update-redis')
@click.option('-p', '--project', required=True)
@click.option('-e', '--environment', required=True)
@click.option('-f', '--feature', required=True)
@click.option('-s', '--state', required=True)
@click_log.simple_verbosity_option(logger)
def updateRedis(project, environment, feature, state):
    hosts = RedisWrapper.connectionStringParser(os.environ.get('REDIS_HOSTS'))

    if len(hosts) < 1:
        raise Exception("REDIS_HOSTS is not set or empty.")

    for host in hosts:
        logger.info("connecting to {0}:{1}".format(host.host, host.port))
        try:
            if validateState(state):
                newState = state.lower()
                r = RedisWrapper(
                    host.host,
                    host.port,
                    logger,
                    project,
                    environment
                )
                r.updateFlagRecord(newState, feature)
                createFile(project, environment, feature, newState)
                logger.info("{0} was successfully updated.".format(feature))
            else:
                raise Exception('Invalid state: {0}, -s needs \
                    to be either on or off.'.format(state))
        except Exception as ex:
            logger.error("unable to update {0}. Exception: {1}".format(
                host.host,
                ex
            ))
            exit(1)


@click.command()
@click_log.simple_verbosity_option(logger)
def playback():
    try:
        executeReplay(logger)
    except Exception:
        logger.error('Unable to Execute Replay.')
        exit(1)


@click.command(name='update-ld-api')
@click.option('-p', '--project', required=True)
@click.option('-e', '--environment', required=True)
@click.option('-f', '--feature', required=True)
@click.option('-s', '--state', required=True)
@click_log.simple_verbosity_option(logger)
def updateLdApi(project, environment, feature, state):
    ld = LaunchDarklyApi(
        os.environ.get('LD_API_KEY'),
        project,
        environment,
        logger
    )

    if validateState(state):
        validState = False if (state.lower() == 'off') else True
        ld.updateFlag(validState, feature)
    else:
        raise Exception('Invalid state: {0}, -s needs to be either \
            on or off.'.format(state))
        exit(1)


@click.command(name='generate-relay-config')
@click.option('-p', '--project', required=True)
@click_log.simple_verbosity_option(logger)
def generateRelayConfig(project):
    """Generate Relay Proxy Configuration

    Generate a ld-relay.conf file to quickly spin up a relay proxy.
    Right now this is mostly used for integration testing.

    :param project: LaunchDarkly project key
    """
    ld = LaunchDarklyApi(
        os.environ.get('LD_API_KEY'),
        projectKey=project,
        logger=logger
    )
    config = ConfigGenerator()

    envs = ld.getEnvironments(project)
    config.generate_relay_config(envs)


cli.add_command(updateRedis)
cli.add_command(playback)
cli.add_command(updateLdApi)
cli.add_command(generateRelayConfig)

if __name__ == '__main__':
    cli()
