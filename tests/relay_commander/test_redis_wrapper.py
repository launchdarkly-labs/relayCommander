import unittest
import logging
from unittest.mock import MagicMock

from relay_commander.redis_wrapper import RedisWrapper


class TestRedis(unittest.TestCase):

    def setUp(self):
        self.redis = RedisWrapper('localhost', 6379, 'support-service', 'brian')

    def test_format_key_name(self):
        formatted_key = 'ld:support-service:brian:features'
        self.assertEqual(formatted_key, self.redis._format_key_name())
        self.redis.redis_key_prefix = 'features'
        self.assertIsNotNone(self.redis._format_key_name())

    def test_get_flag_record(self):
        self.assertIsNotNone(self.redis.get_flag_record('show-widgets'))
        # test unknown flag key raises exception
        with self.assertRaises(Exception):
            self.redis.get_flag_record('test')

    def test_connection_string_parser(self):
        # single box, default port
        hosts = self.redis.connection_string_parser('localhost')

        self.assertEqual(len(hosts), 1)

        for host in hosts:
            self.assertEqual(host.host, 'localhost')
            self.assertEqual(host.port, 6379)

        # single box with comma, default port
        hosts = self.redis.connection_string_parser('localhost,')

        self.assertEqual(len(hosts), 1)

        for host in hosts:
            self.assertEqual(host.host, 'localhost')
            self.assertEqual(host.port, 6379)

        # single box, other port
        hosts = self.redis.connection_string_parser('localhost:6231')

        self.assertEqual(len(hosts), 1)

        for host in hosts:
            self.assertEqual(host.host, 'localhost')
            self.assertEqual(host.port, 6231)

        # single box with comma, other port
        hosts = self.redis.connection_string_parser('localhost:6231,')

        self.assertEqual(len(hosts), 1)

        for host in hosts:
            self.assertEqual(host.host, 'localhost')
            self.assertEqual(host.port, 6231)

        # multi box, default port
        hosts = self.redis.connection_string_parser('localhost,localhost')

        self.assertEqual(len(hosts), 2)

        for host in hosts:
            self.assertEqual(host.host, 'localhost')
            self.assertEqual(host.port, 6379)

        # multi box, other port
        hosts = self.redis.connection_string_parser('localhost:6211,localhost:6211')

        self.assertEqual(len(hosts), 2)

        for host in hosts:
            self.assertEqual(host.host, 'localhost')
            self.assertEqual(host.port, 6211)

        # complete mix
        hosts = self.redis.connection_string_parser('localhost, localhost:6379, localhost:4321, localhost,')

        self.assertEqual(len(hosts), 4)

        for host in hosts:
            self.assertEqual(host.host, 'localhost')

        self.assertEqual(hosts[0].port, 6379)
        self.assertEqual(hosts[1].port, 6379)
        self.assertEqual(hosts[2].port, 4321)
        self.assertEqual(hosts[3].port, 6379)

        # test runtime error raises exception
        with self.assertRaises(RuntimeError):
            self.redis.connection_string_parser('localhost:6379:00')

    def test_update_flag_record(self):
        self.redis.update_flag_record('on', 'show-widgets')