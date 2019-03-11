import unittest
import glob
import shutil
import os

from relay_commander.replay_builder import check_local, create_file

class TestReplayBuilder(unittest.TestCase):

    def tearDown(self):
        shutil.rmtree('./replay')

    def test_check_local(self):
        to_check = ['./replay', './replay/toDo', './replay/archive']

        check_local()

        for i in to_check:
            self.assertTrue(os.path.exists(i))

    def test_create_file(self):
        create_file('test', 'test', 'test', 'true')
        create_file('test', 'test', 'test', 'false')

        files = glob.glob('./replay/toDo/*')

        assert len(files) > 0

        with open(files[0], 'r') as f:
            file_content = f.read()
            assert 'test' in file_content
            assert 'update-ld-api' in file_content
            assert 'rc' in file_content

        # test file names unique
        assert files[0] != files[1]
