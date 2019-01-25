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
    rawHosts = os.environ.get('REDIS_HOSTS')
    rawHostList = rawHosts.split(",")
    hosts = [host for host in rawHostList if len(host) > 0]

    for host in hosts:
        logger.info(len(host))
        logger.info("connecting to {0}".format(host))
        try:
            if validateState(state):
                newState = False if (state.lower() == 'false') else True
                r = RedisWrapper(host, logger, project, environment)
                r.updateFlagRecord(newState, feature)
                createFile(project, environment, feature, newState)
                logger.info("{0} was successfully updated.".format(feature))
            else:
                logger.error("Invalid state: {0}, -s needs to be either true or false.".format(state))
        except Exception as ex:
            logger.error("unable to update {0}. Exception: {1}".format(host, ex))

@click.command()
@click_log.simple_verbosity_option(logger)
def playback():
    executeReplay()
    click.echo("LaunchDarkly is now update to date")

@click.command(name='update-ld-api')
@click.option('-p', '--project', required=True)
@click.option('-e', '--environment', required=True)
@click.option('-f', '--feature', required=True)
@click.option('-s', '--state', required=True)
@click_log.simple_verbosity_option(logger)
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
