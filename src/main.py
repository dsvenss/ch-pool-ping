from PoolTableChecker import PoolTableChecker
import mattermost_client
import CommandHandler
import ConfigHandler
import camera
import time
from pathlib import Path
import Logger

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
            Util.exception(e)
    
    if isAvailable != wasAvailable:
        mattermost_client.updateMattermostAvailable(isAvailable)
    
    wasAvailable = isAvailable
    
    currentImage.rename(oldImagePath)

while True:
    try:
        camera.takePicture()
        CommandHandler.reactToCommands()
        checkAvailability()
    except Exception as e:
        Logger.exception(e)
    time.sleep(CommandHandler.getInterval())
