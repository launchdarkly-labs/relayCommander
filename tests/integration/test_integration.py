import os
import subprocess
import time
import unittest

from click.testing import CliRunner

from relay_commander.ld import LaunchDarklyApi
from relay_commander.rc import generate_relay_config, playback, update_redis
from relay_commander.redis_wrapper import RedisWrapper


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
            update_redis,
            ['-p', 'support-service', '-e', 'lev', '-f',
                'relay-commander-integration-test', '-s', newState]
        )
        print(result.output)
        self.assertEqual(result.exit_code, 0)

        # playback
        result = runner.invoke(
            ['-v', 'DEBUG'],
            playback,
        )
        print(result.output)
        self.assertEqual(result.exit_code, 0)
