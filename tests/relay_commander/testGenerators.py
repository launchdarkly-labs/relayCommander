import unittest

from relay_commander.generators import ConfigGenerator


class TestGenerators(unittest.TestCase):

    def setUp(self):
        self.configGenerator = ConfigGenerator()

    def testInit(self):
        self.assertIsInstance(self.configGenerator, ConfigGenerator)
