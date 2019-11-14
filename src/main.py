from PoolTableChecker import PoolTableChecker
import mattermost_client
import CommandHandler
import ConfigHandler
import camera
import time
from pathlib import Path
from shutil import copyfile
import Logger
from ScoreKeeper import ScoreKeeper

wasAvailable = False
pooltableChecker = PoolTableChecker()
 
def checkAvailability():
    global wasAvailable
    global pooltableChecker
    oldImagePath = ConfigHandler.getOldImagePath()
    currentImagePath = ConfigHandler.getCurrentImagePath()
    isAvailable = True
    
    currentImage = Path(currentImagePath)
    oldImage = Path(oldImagePath)

    Logger.info("Comparing images")
    
    if oldImage.is_file():
        try:
            isAvailable = pooltableChecker.isTableFree(currentImagePath, oldImagePath)
        except Exception as e:
            isAvailable = None
            Logger.exception(e)
    
    if isAvailable != wasAvailable:
        Logger.info('Posting availability: ' + str(isAvailable))
        mattermost_client.updateMattermostAvailable(isAvailable)
    
    wasAvailable = isAvailable
    copyfile(currentImagePath, ConfigHandler.getRawImagePath())
    currentImage.rename(oldImagePath)

mattermost_client.postToCommandChannel("Pool-ping is up and running")

while CommandHandler.getRunMain():
    try:
        time.sleep(CommandHandler.getInterval())
        camera.takePicture()
        checkAvailability()
        CommandHandler.reactToCommands()
    except Exception as e:
        Logger.exception(e)
    
    
mattermost_client.postToCommandChannel("Pool-ping is shutdown")