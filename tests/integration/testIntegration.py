import unittest

from subprocess import run
from click.testing import CliRunner


class TestIntegration(unittest.TestCase):

    def setUp(self):
        run(
            ['source .env &&', 'rc', 'generate-relay-config', '-p', 'support-service'],
            shell=True,
            check=True
            )
        run(
            ['docker-compose', '-f', 'docker-compose.relay.yml', 'up', '-d'],
            shell=True,
            check=True
        )

    def tearDown(self):
        run(
            ['docker-compose', 'down'],
            shell=True,
            check=True
        )

    def testInit(self):
        self.assertTrue(True)
