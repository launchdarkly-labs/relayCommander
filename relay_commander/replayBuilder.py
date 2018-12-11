import os

def createDirectories(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def checkLocal():
    toCheck = ['../replay', '../replay/toDo', '../replay/archive']
    
    for i in toCheck:
        createDirectories(i)

def replayFile():
    

checkLocal()
# check to see if directories are created: 
# write a new file to local directory with RC command
# when replay is run, move from to archived directory
# 