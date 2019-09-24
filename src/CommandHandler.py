import mattermost_client

thGreenLow = [30,100,100]
thGreenHigh = [90,255,255]
sensitivity = 0.02

def updateSettings():
    global thGreenLow
    global thGreenHigh
    
    commands = mattermost_client.getCommands()
    print(commands)
    for cmd in commands:
        command = cmd['command']
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
    
def getThGreenLow():
    global thGreenLow
    return thGreenLow

def getThGreenHigh():
    global thGreenHigh
    return thGreenHigh

def getSensitivity():
    global sensitivity
    return sensitivity


updateSettings()