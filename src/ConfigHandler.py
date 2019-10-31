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

def getGitRepo():
    return "https://github.com/dsvenss/ch-pool-ping.git"

def setConfig(key, value):
    config = getMattermostConfig()
    config[key] = value
    with open("../mattermostConfig.yml", "w") as outfile:
        yaml.dump(config, outfile, default_flow_style=False)