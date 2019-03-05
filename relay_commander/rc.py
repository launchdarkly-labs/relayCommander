"""Relay Commander CLI
"""
import logging
import os
import subprocess
import sys

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
                r = RedisWrapper(host.host, host.port, logger, project, environment)
                r.updateFlagRecord(newState, feature)
                createFile(project, environment, feature, newState)
                logger.info("{0} was successfully updated.".format(feature))
            else:
                raise Exception('Invalid state: {0}, -s needs to be either on or off.'.format(state))
        except Exception as ex:
            logger.error("unable to update {0}. Exception: {1}".format(host.host, ex))

@click.command()
@click_log.simple_verbosity_option(logger)
def playback():
    try:
        executeReplay(logger)
    except:
        logger.error('Unable to Execute Replay.')

@click.command(name='update-ld-api')
@click.option('-p', '--project', required=True)
@click.option('-e', '--environment', required=True)
@click.option('-f', '--feature', required=True)
@click.option('-s', '--state', required=True)
@click_log.simple_verbosity_option(logger)
def updateLdApi(project, environment, feature, state):
    ld = LaunchDarklyApi(os.environ.get('LD_API_KEY'), project, environment, logger)

    if validateState(state):
        validState = False if (state.lower() == 'off') else True
        ld.updateFlag(validState, feature)
    else:
        raise Exception('Invalid state: {0}, -s needs to be either on or off.'.format(state))

cli.add_command(updateRedis)
cli.add_command(playback)
cli.add_command(updateLdApi)

if __name__ == '__main__':
    cli()
