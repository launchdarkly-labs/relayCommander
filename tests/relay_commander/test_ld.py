import unittest

from relay_commander.ld import LaunchDarklyApi


class TestLd(unittest.TestCase):

    def setUp(self):
        self.ld = LaunchDarklyApi('test', 'test', 'test')

    def test_init(self):
        self.assertIsInstance(self.ld, LaunchDarklyApi)
