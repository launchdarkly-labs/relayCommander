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
		file_object.write('rc update-ld-api -p {0} -e {1} -f {2} -s {3}'.format(project, environment, feature, state)

def executeReplay():
	"""Will itereate through files created in ./replay/toDO and move them to archive.
	"""
	path = './replay/toDo/'
	getFiles = os.listdir(path)
	getFiles = [os.path.join(path, file) for file in getFiles]
	sortFiles = sorted(getFiles, key=os.path.getctime)
	
	for i in sortFiles:
		getFile = open(i)
		runUpdate = getFile.read()
		run(runUpdate, shell=True)
		getFile.close()
		moveFile = 'mv {0} ./replay/archive/'.format(i)
		run(moveFile, shell=True)