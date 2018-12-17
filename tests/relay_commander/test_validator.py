import unittest

from relay_commander.validator import validateState


class TestValidator(unittest.TestCase):

    def test_invalid_input(self):
        result = validateState('bad')
        self.assertFalse(result)
    
    def test_valid_input(self):
        result = validateState('true')
        self.assertTrue(result)

        result = validateState('false')
        self.assertTrue(result)
    
    def test_valid_input_mixcase(self):
        result = validateState('TrUe')
        self.assertTrue(result)

        result = validateState('FaLSE')
        self.assertTrue(result)