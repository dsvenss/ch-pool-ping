from PoolTableChecker import PoolTableChecker
import mattermost_client
import CommandHandler
import camera
import time
from pathlib import Path
import Util

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
    
    Util.log("Comparing images")
    if oldImage.is_file():
        try:
            isAvailable = pooltableChecker.isTableFree(currentImagePath, oldImagePath)
        except Exception as e:
            Util.log(str(e))
    
    if isAvailable != wasAvailable:
        mattermost_client.updateMattermostAvailable(isAvailable)
    
    wasAvailable = isAvailable
    
    currentImage.rename(oldImagePath)

while True:
    try:
        camera.takePicture()
        CommandHandler.updateSettings()
        checkAvailability()
    except Exception as e:
        Util.log(str(e))
    time.sleep(CommandHandler.getInterval())
