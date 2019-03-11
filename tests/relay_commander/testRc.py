import unittest

from click.testing import CliRunner

from relay_commander.rc import cli


class TestRc(unittest.TestCase):

    def setUp(self):
        pass

    def testMainCli(self):
        runner = CliRunner()
        result = runner.invoke(cli)

        self.assertTrue(result.exit_code == 0)
