import glob
import os
import uuid
from subprocess import run


def checkLocal():
    """Check for directories and create if not already there
    """
    toCheck = ['./replay', './replay/toDo', './replay/archive']

    for i in toCheck:
        if not os.path.exists(i):
            os.makedirs(i)


def createFile(project, environment, feature, state):
    """Create file with RC command that will be called against LaunchDarkly API.

    :param Project: LaunchDarkly Project
    :param environment: LaunchDarkly Environment
    :param feature: LaunchDarkly Feature
    :param state: State to update feature flag
    """
    checkLocal()
    savePath = './replay/toDo/'
    filename = '{0}.txt'.format(str(uuid.uuid1()))
    completeName = os.path.join(savePath, filename)

    with open(completeName, 'w') as file_object:
        file_object.write('rc update-ld-api \
            -p {0} -e {1} -f {2} -s {3}'.format(
            project,
            environment,
            feature,
            state
        ))


def executeReplay(logger=None):
    """Execute commands

    1. Itereate through files created in ./replay/toDO
    2. Execute the command inside each file
    3. Move the file to the archive.
    """
    files = glob.glob('./replay/toDo/*')
    sortedFiles = sorted(files, key=os.path.getctime)

    if len(sortedFiles) > 0:
        logger.debug('Found {0}, beginning execution.'.format(sortedFiles))
        for commandFile in sortedFiles:
            with open(commandFile, 'r') as command:
                cmd = command.read()
                logger.debug('executing command: {0}'.format(cmd))
                resp = run([cmd, '-v', 'DEBUG'], shell=True, check=True)
                logger.debug(resp)
                logger.debug('moving {0} to archive'.format(command.name))
                moveCommand = 'mv {0} ./replay/archive/'.format(command.name)
                run(moveCommand, shell=True, check=True)
        logger.info('LaunchDarkly is now up to date.')
    else:
        logger.warning('No files found, nothing to replay.')
