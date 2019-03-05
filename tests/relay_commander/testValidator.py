import unittest

from relay_commander.validator import validateState


class TestValidator(unittest.TestCase):

    def testInvalidInput(self):
        result = validateState('bad')
        self.assertFalse(result)
    
    def testValidInput(self):
        result = validateState('on')
        self.assertTrue(result)

        result = validateState('off')
        self.assertTrue(result)
    
    def testValidInputMixcase(self):
        result = validateState('oN')
        self.assertTrue(result)

        result = validateState('OfF')
        self.assertTrue(result)