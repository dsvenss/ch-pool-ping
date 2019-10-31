from PoolTableChecker import PoolTableChecker
import mattermost_client
import CommandHandler
import ConfigHandler
import camera
import time
from pathlib import Path
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
    
    currentImage.rename(oldImagePath)


mattermost_client.postToCommandChannel("Pool-ping is up and running")

while CommandHandler.getRunMain():
    try:
        camera.takePicture()
        CommandHandler.reactToCommands()
        checkAvailability()
    except Exception as e:
        Logger.exception(e)
    time.sleep(CommandHandler.getInterval())
    
mattermost_client.postToCommandChannel("Pool-ping is shutdown")