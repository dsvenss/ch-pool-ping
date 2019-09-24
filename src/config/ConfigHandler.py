import yaml

mattermostConfig = None


def getMattermostConfig():
    global mattermostConfig
    if not mattermostConfig:
        rawConfig = open("../mattermostConfig.yml", "r")
        mattermostConfig = yaml.load(rawConfig, Loader=yaml.FullLoader)
    return mattermostConfig
