import unittest
import logging
from unittest.mock import MagicMock

from relay_commander.redis import RedisWrapper

logger = logging.getLogger(__name__)

class TestRedis(unittest.TestCase):

    def setUp(self):
        self.redis = RedisWrapper(logger, 'test', 'test')

    def testFormatKeyName(self):
        formattedKey = 'ld:test:test:features'
        self.assertEqual(formattedKey, self.redis._formatKeyName())

    def testGetFlagRecord(self):
        # test unknown flag key raises exception
        with self.assertRaises(Exception):
            flag = self.redis.getFlagRecord('test')
