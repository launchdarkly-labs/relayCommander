from subprocess import run

import os
import uuid



def createDirectories(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def checkLocal():
    toCheck = ['../replay', '../replay/toDo', '../replay/archive']
    
    for i in toCheck:
        createDirectories(i)

def createFile(project, environment, feature, state):
    savePath = 'replay/toDo/'
    filename = str(uuid.uuid1()) + '.txt'
    completeName = os.path.join(savePath, filename)

    with open(completeName, 'w') as file_object:
        file_object.write('rc ld-api -p ' + project + ' -e ' + environment + ' -f ' + feature + ' -s ' + state)

def executeReplay():
    # get list of files in directory
    path = './replay/toDo/'

    # order from oldest to newest
    getFiles = os.listdir(path)
    getFiles = [os.path.join(path, file) for file in getFiles]
    sortFiles = sorted(getFiles, key=os.path.getctime)

    # iterate through list of files
    for i in sortFiles:
        getFile = open(i)

        runUpdate = getFile.read()
    # once file is accessed, execute the command within their
        run(runUpdate, shell=True)

    # after executed, move the file to archive directory
        getFile.close()
        moveFile = 'mv ' + i + ' ./replay/archive/'
        run(moveFile, shell=True)

