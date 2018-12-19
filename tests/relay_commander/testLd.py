import unittest

from relay_commander.ld import LaunchDarklyApi


class TestLd(unittest.TestCase):

    def setUp(self):
        self.ld = LaunchDarklyApi('test', 'test', 'test')

    def testInit(self):
        self.assertIsInstance(self.ld, LaunchDarklyApi)
        
    def testFormatHostname(self):
        formattedHostname = self.ld.formatHostname('test')
        assert 'test' in formattedHostname