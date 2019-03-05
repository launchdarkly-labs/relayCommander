import os
import subprocess
import time
import unittest

from click.testing import CliRunner

from relay_commander.ld import LaunchDarklyApi
from relay_commander.rc import generateRelayConfig, playback, updateRedis
from relay_commander.redis import RedisWrapper


class TestIntegration(unittest.TestCase):

    def testIntegration(self):
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
            updateRedis,
            ['-p', 'support-service', '-e', 'lev', '-f',
                'relay-commander-integration-test', '-s', newState]
        )
        print(result.output)
        self.assertEqual(result.exit_code, 0)

        # playback
        result = runner.invoke(
            playback,
            ['-v', 'DEBUG']
        )
        print(result.output)
        self.assertEqual(result.exit_code, 0)
