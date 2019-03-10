import unittest
import os

from relay_commander.validator import valid_state, valid_env_vars, _check_env_var


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

    def test_check_env_var(self):
        # ENV VAR not set
        with self.assertRaises(KeyError):
            _check_env_var('DOES_NOT_EXIST')

        # ENV VAR set but empty
        os.environ['EMPTY'] = ""
        with self.assertRaises(KeyError):
            _check_env_var('EMPTY')

        # ENV VAR set and not empty
        os.environ['SET'] = "test"
        self.assertTrue(_check_env_var("SET"))

    def test_valid_env_vars(self):
        with self.assertRaises(SystemExit):
            valid_env_vars()
