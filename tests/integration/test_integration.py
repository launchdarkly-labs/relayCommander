import os
import subprocess
import time
import unittest

from click.testing import CliRunner

from relay_commander.ld import LaunchDarklyApi
from relay_commander.rc import generate_relay_config, playback, update_redis, cli, update_dynamodb, update
from relay_commander.redis_wrapper import RedisWrapper
from relay_commander.DynamoDB_wrapper import DdbWrapper


class TestIntegration(unittest.TestCase):

    def test_integration(self):
        # working with relay-commander-integration-test flag

        # get current flag state from LD
        ld = LaunchDarklyApi(os.environ.get('LD_API_KEY'), 'support-service')
        flag = ld.feature.get_feature_flag(
            'support-service', 'relay-commander-integration-test', env="lev")
        state = flag.environments['lev'].on

        if state == True:
            newState = 'off'
        else:
            newState = 'on'

        # update redis
        runner = CliRunner()
        result = runner.invoke(
            update,
            ['-d', 'redis', '-p', 'support-service', '-e', 'brian', '-f',
                'show-widgets', '-s', newState]
        )
        print(result.output)
        self.assertEqual(result.exit_code, 0)

        ddb_result = runner.invoke(
            update,
            ['-d', 'dynamodb', '-p', 'support-service', '-e', 'brian', '-f',
                'show-widgets', '-s', newState, '-t', 'ld-relay']
        )
        print(ddb_result.output)
        self.assertEqual(ddb_result.exit_code, 0)
        
        # playback
        result = runner.invoke(
            cli,
            ['-v', 'DEBUG', 'playback'],
        )
        print(result.output)
        self.assertEqual(result.exit_code, 0)
