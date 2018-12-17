import unittest

from relay_commander.validator import validateState


class TestValidator(unittest.TestCase):

    def testInvalidInput(self):
        result = validateState('bad')
        self.assertFalse(result)
    
    def testValidInput(self):
        result = validateState('true')
        self.assertTrue(result)

        result = validateState('false')
        self.assertTrue(result)
    
    def testValidInputMixcase(self):
        result = validateState('TrUe')
        self.assertTrue(result)

        result = validateState('FaLSE')
        self.assertTrue(result)