import unittest
import logging
from unittest.mock import MagicMock

from relay_commander.redis import RedisWrapper

logger = logging.getLogger(__name__)

class TestRedis(unittest.TestCase):

    def setUp(self):
        self.redis = RedisWrapper('localhost', 6379, logger, 'test', 'test')

    def testFormatKeyName(self):
        formattedKey = 'ld:test:test:features'
        self.assertEqual(formattedKey, self.redis._formatKeyName())

    def testGetFlagRecord(self):
        # test unknown flag key raises exception
        with self.assertRaises(Exception):
            flag = self.redis.getFlagRecord('test')

    def testConnectionStringParser(self):
        # single box, default port 
        hosts = self.redis.connectionStringParser('localhost')

        self.assertEqual(len(hosts), 1)

        for host in hosts:
            self.assertEqual(host.host, 'localhost')
            self.assertEqual(host.port, 6379)

        # single box with comma, default port 
        hosts = self.redis.connectionStringParser('localhost,')

        self.assertEqual(len(hosts), 1)

        for host in hosts:
            self.assertEqual(host.host, 'localhost')
            self.assertEqual(host.port, 6379)

        # single box, other port 
        hosts = self.redis.connectionStringParser('localhost:6231')

        self.assertEqual(len(hosts), 1)

        for host in hosts:
            self.assertEqual(host.host, 'localhost')
            self.assertEqual(host.port, 6231)

        # single box with comma, other port 
        hosts = self.redis.connectionStringParser('localhost:6231,')

        self.assertEqual(len(hosts), 1)

        for host in hosts:
            self.assertEqual(host.host, 'localhost')
            self.assertEqual(host.port, 6231)

        # multi box, default port 
        hosts = self.redis.connectionStringParser('localhost,localhost')

        self.assertEqual(len(hosts), 2)

        for host in hosts:
            self.assertEqual(host.host, 'localhost')
            self.assertEqual(host.port, 6379)

        # multi box, other port 
        hosts = self.redis.connectionStringParser('localhost:6211,localhost:6211')

        self.assertEqual(len(hosts), 2)

        for host in hosts:
            self.assertEqual(host.host, 'localhost')
            self.assertEqual(host.port, 6211)

        # complete mix
        hosts = self.redis.connectionStringParser('localhost, localhost:6379, localhost:4321, localhost,')

        self.assertEqual(len(hosts), 4)
    
        for host in hosts:
            self.assertEqual(host.host, 'localhost')

        self.assertEqual(hosts[0].port, 6379)
        self.assertEqual(hosts[1].port, 6379)
        self.assertEqual(hosts[2].port, 4321)
        self.assertEqual(hosts[3].port, 6379)