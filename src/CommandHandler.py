from ScoreKeeper import ScoreKeeper
import mattermost_client
import Logger
import SyncHandler
import numpy
import ConfigHandler

thGreenLow = [25, 52, 72]
thGreenHigh = [90, 255, 255]
bounds = numpy.array([
    [[520, 590]],
    [[850, 490]],
    [[1380, 740]],
    [[970, 960]]
])
sensitivity = 0.09
interval = 30
runMain = True

def reactToCommands():
    global thGreenLow
    global thGreenHigh
    global sensitivity
    global interval
    global runMain
    global bounds

    Logger.info("Getting commands")
    commands = mattermost_client.getCommands()
    for cmd in commands:
        command = cmd['command']
        extraMsg = ''
        Logger.info("Reacting to command: " + command)

        if command == 'setThGreenLow':
            thGreenLow[0] = int(cmd['h'])
            thGreenLow[1] = int(cmd['s'])
            thGreenLow[2] = int(cmd['v'])
        elif command == 'setThGreenHigh':
            thGreenHigh[0] = int(cmd['h'])
            thGreenHigh[1] = int(cmd['s'])
            thGreenHigh[2] = int(cmd['v'])
        elif command == 'setSensitivity':
            sensitivity = float(cmd['value'])
        elif command == 'getImage':
            mattermost_client.postCroppedImage()
        elif command == 'getRawImage':
            mattermost_client.postRawImage()
        elif command == 'getIp':
            mattermost_client.postIP()
        elif command == 'setInterval':
            interval = int(cmd['value'])
        elif command == 'getLog':
            log = Logger.getLog()
            mattermost_client.postLog(log)
        elif command == 'getScore':
            mattermost_client.postScore()
        elif command == 'sync':
            SyncHandler.syncSystem()
            runMain = False
        elif command == 'clearHistory':
            mattermost_client.clearCommandChannelHistory(0)
        elif command == 'setConfig':
            key = str(cmd['key'])
            value = str(cmd['value'])
            ConfigHandler.setConfig(key, value)
        elif command == 'getConfig':
            key = str(cmd['key'])
            config = ConfigHandler.getMattermostConfig()
            value = config[key]
            mattermost_client.postConfig(key, value)
        elif command == 'setBounds':
            bounds = numpy.array([
                [[int(cmd['c1x']), int(cmd['c1y'])]],
                [[int(cmd['c2x']), int(cmd['c2y'])]],
                [[int(cmd['c3x']), int(cmd['c3y'])]],
                [[int(cmd['c4x']), int(cmd['c4y'])]]
                ])
        elif command == 'dumpConfig':
            currentConfig = """
Sensitivity: {sensitivity}
Interval: {interval}
ThGreenLow: {thGreenLow}
ThGreenHigh: {thGreenHigh}
Current score: {score}
Bounds: {bounds}
""".format(
                sensitivity=str(sensitivity),
                interval=str(interval),
                thGreenLow=str(thGreenLow),
                thGreenHigh=str(thGreenHigh),
                score=str(ScoreKeeper.score),
                bounds=str(bounds)
            )
            mattermost_client.postCurrentConfig(currentConfig)
        else:
            extraMsg = ' [UNKNOWN]'

        mattermost_client.postToCommandChannel("Command handled: " + command + extraMsg)

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
    
