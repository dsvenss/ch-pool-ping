import mattermost_client
import Logger

thGreenLow = [35,100,100]
thGreenHigh = [86,255,255]
sensitivity = 0.02
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
            thGreenLow[0] = cmd['r']
            thGreenLow[1] = cmd['g']
            thGreenLow[2] = cmd['b']
        elif command == 'thGreenHigh':
            thGreenHigh[0] = cmd['r']
            thGreenHigh[1] = cmd['g']
            thGreenHigh[2] = cmd['b']
        elif command == 'sensitivity':
            sensitivity = cmd['value']
        elif command == 'getImage':
            mattermost_client.postImage()
        elif command == 'getIp':
            mattermost_client.postIP()
        elif command == 'updateInterval':
            interval = int(cmd['value'])
        elif command == 'getLog':
            mattermost_client.postLog()
        
    
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