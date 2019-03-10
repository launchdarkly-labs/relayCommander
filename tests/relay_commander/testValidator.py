import unittest

from relay_commander.validator import valid_state, valid_env_vars


class TestValidator(unittest.TestCase):

    def testInvalidInput(self):
        result = valid_state('bad')
        self.assertFalse(result)

    def testValidInput(self):
        result = valid_state('on')
        self.assertTrue(result)

        result = valid_state('off')
        self.assertTrue(result)

    def testValidInputMixcase(self):
        result = valid_state('oN')
        self.assertTrue(result)

        result = valid_state('OfF')
        self.assertTrue(result)
