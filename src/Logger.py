import logging
import ConfigHandler
import os
import mattermost_client as mattermost

logger = logging.getLogger("pool-ping")
fileLogger = logging.FileHandler(ConfigHandler.getLogPath())
fileLogger.setLevel(logging.DEBUG)
fileLogger.setFormatter(logging.Formatter(fmt='%(name)s - %(asctime)s # %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S'))
logger.addHandler(fileLogger)

def info(msg):
    print(msg)
    
def error(msg):
    print(msg)
    mattermost.postError(msg)

def exception(e):
    print(e)
    mattermost.postError(str(e))
    
def getLog():
    try:
        path = ConfigHandler.getLogPath()
        logFile = open(path, "r+")
        logFile.seek(0, os.SEEK_END)
        logFile.seek(logFile.tell() - 500, os.SEEK_SET)
        line = logFile.readline()
        logText = ""
        while line:
            logText += line
            line = logFile.readline()
        return logText
    finally:
        logFile.close()
