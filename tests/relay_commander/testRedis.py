import unittest
from unittest.mock import MagicMock

from relay_commander.redis import RedisWrapper
from relay_commander.ld import LaunchDarklyApi

class TestRedis(unittest.TestCase):

    ld = MagicMock(spec=LaunchDarklyApi)
    ld.projectKey = 'test'
    ld.environmentKey = 'test'

    def setUp(self):
        self.redis = RedisWrapper(self.ld)

    def testGetFlagRecord(self):

        # test unknown flag key raises exception
        with self.assertRaises(Exception):
            flag = self.redis.getFlagRecord('test')
