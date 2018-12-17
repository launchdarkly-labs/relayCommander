import unittest
import glob
import shutil

from relay_commander.replayBuilder import *
from click.testing import CliRunner

class TestReplayBuilder(unittest.TestCase):

    def tearDown(self):
        shutil.rmtree('./replay')

    def testCheckLocal(self):
        toCheck = ['./replay', './replay/toDo', './replay/archive']

        checkLocal()

        for i in toCheck:
            self.assertTrue(os.path.exists(i))

    def testCreateFile(self):
        createFile('test', 'test', 'test', 'true')
        createFile('test', 'test', 'test', 'false')

        files = glob.glob('./replay/toDo/*')

        assert len(files) > 0

        with open(files[0], 'r') as f:
            fileContent = f.read()
            assert 'test' in fileContent
            assert 'update-ld-api' in fileContent
            assert 'rc' in fileContent

        # test file names unique
        assert files[0] != files[1]