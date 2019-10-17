import mattermost_client
import Logger

thGreenLow = [25,52,72]
thGreenHigh = [90,255,255]
sensitivity = 0.01
interval = 3

def reactToCommands():
    global thGreenLow
    global thGreenHigh
    global sensitivity
    global interval
    
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