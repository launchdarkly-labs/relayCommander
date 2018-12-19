import unittest
from unittest.mock import MagicMock

from relay_commander.redis import RedisWrapper

class TestRedis(unittest.TestCase):

    def setUp(self):
        self.redis = RedisWrapper('test', 'test')

    def testFormatKeyName(self):
        formattedKey = 'ld:test:test:features'
        self.assertEqual(formattedKey, self.redis._formatKeyName())

    def testGetFlagRecord(self):
        # test unknown flag key raises exception
        with self.assertRaises(Exception):
            flag = self.redis.getFlagRecord('test')
