import mattermost_client
import Logger
import SyncHandler
import numpy

thGreenLow = [25, 52, 72]
thGreenHigh = [90, 255, 255]
bounds = []
sensitivity = 0.01
interval = 3
runMain = True

def reactToCommands():
    global thGreenLow
    global thGreenHigh
    global sensitivity
    global interval
    global runMain
    global bounds

    commands = mattermost_client.getCommands()
    for cmd in commands:
        command = cmd['command']
        Logger.info("Reacting to command: " + command)

        if command == 'thGreenLow':
            thGreenLow[0] = cmd['h']
            thGreenLow[1] = cmd['s']
            thGreenLow[2] = cmd['v']
        elif command == 'thGreenHigh':
            thGreenHigh[0] = cmd['h']
            thGreenHigh[1] = cmd['s']
            thGreenHigh[2] = cmd['v']
        elif command == 'sensitivity':
            sensitivity = cmd['value']
        elif command == 'getImage':
            mattermost_client.postCroppedImage()
        elif command == 'getRawImage':
            mattermost_client.postRawImage()
        elif command == 'getIp':
            mattermost_client.postIP()
        elif command == 'updateInterval':
            interval = int(cmd['value'])
        elif command == 'getLog':
            mattermost_client.postLog()
        elif command == 'getScore':
            mattermost_client.postScore()
        elif command == 'sync':
            SyncHandler.syncSystem()
            runMain = False
        elif command == 'setBounds':
            bounds = numpy.array([
                [[int(cmd['c1x']), int(cmd['c1y'])]],
                [[int(cmd['c2x']), int(cmd['c2y'])]],
                [[int(cmd['c3x']), int(cmd['c3y'])]],
                [[int(cmd['c4x']), int(cmd['c4y'])]]
                ])

def areBoundsSet():
    return len(bounds) > 0

def getBounds():
    return bounds

def getThGreenLow():
    global thGreenLow
    return thGreenLow

def getThGreenHigh():
    global thGreenHigh
    return thGreenHigh

def getSensitivity():
    global sensitivity
    return sensitivity

def getInterval():
    global interval
    return interval

def getRunMain():
    global runMain
    return runMain
    