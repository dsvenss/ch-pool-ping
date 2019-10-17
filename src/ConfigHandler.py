import yaml

mattermostConfig = None

def getMattermostConfig():
    global mattermostConfig
    if not mattermostConfig:
        rawConfig = open("../mattermostConfig.yml", "r")
        mattermostConfig = yaml.load(rawConfig, Loader=yaml.FullLoader)
    return mattermostConfig

def getCurrentImagePath():
    return 'current.jpg'

def getOldImagePath():
    return 'old.jpg'

def getLogPath():
    return 'pool-ping.log'

def getCroppedImagePath():
    return 'croppedImage.jpg'