# -*- coding: utf-8 -*-
"""
relay_commander.replay_builder
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This module provides functionality to generate the replay directory and
keep track of pending and completed API calls.

As a part of the runbook, when a user makes a change directly to redis we
make a copy of the command that they need to run in order to update the API
when LaunchDarkly connectivity resumes.

These commands are stored in a directory called ``replay`` which has the
following structure:

.. code-block:: bash

    replay
    ├── archive
    └── toDo

.. versionchanged: 0.0.12
    * refactor to conform with pep-8 and pep-484
"""
import glob
import os
import uuid
from subprocess import run

from relay_commander.util import LOG


def check_local() -> None:
    """
    Verify required directories exist.

    This functions checks the current working directory to ensure that
    the required directories exist. If they do not exist, it will create them.
    """
    to_check = ['./replay', './replay/toDo', './replay/archive']

    for i in to_check:
        if not os.path.exists(i):
            os.makedirs(i)


def create_file(project: str, environment: str, feature: str, state: str) -> None:
    """
    Create file to replay.

    Create file with ``rc`` command that will be called against the
    LaunchDarkly API when ``rc playback`` is called from the main CLI.

    :param project: LaunchDarkly Project
    :param environment: LaunchDarkly Environment
    :param feature: LaunchDarkly Feature
    :param state: State to update feature flag
    """
    check_local()
    save_path = './replay/toDo/'
    filename = '{0}.txt'.format(str(uuid.uuid1()))
    complete_name = os.path.join(save_path, filename)

    with open(complete_name, 'w') as filename:
        filename.write('rc update-ld-api -p {0} -e {1} -f {2} -s {3}'.format(
            project,
            environment,
            feature,
            state
        ))


def execute_replay() -> None:
    """
    Execute all commands.

    For every command that is found in replay/toDo, execute each of them
    and move the file to the replay/archive directory.
    """
    files = glob.glob('./replay/toDo/*')
    sorted_files = sorted(files, key=os.path.getctime)

    if not sorted_files:  # list is not empty
        LOG.debug('Found %s, beginning execution.', sorted_files)
        for command_file in sorted_files:
            with open(command_file, 'r') as command:
                cmd = command.read()
                LOG.debug('executing command: %s', cmd)
                resp = run([cmd, '-v', 'DEBUG'], shell=True, check=True)
                LOG.debug(resp)
                LOG.debug('moving %s to archive', command.name)
                move_command = 'mv {0} ./replay/archive/'.format(command.name)
                run(move_command, shell=True, check=True)
        LOG.info('LaunchDarkly is now up to date.')
    else:
        LOG.warning('No files found, nothing to replay.')
