from PoolTableChecker import PoolTableChecker
import mattermost_client
import CommandHandler
import camera
import time
from pathlib import Path
import Util

CURRENT_IMAGE = "current.jpg"
OLD_IMAGE = "old.jpg"

wasAvailable = False
pooltableChecker = PoolTableChecker()
 
def checkAvailability():
    global wasAvailable
    global pooltableChecker
    isAvailable = True
    camera.takePicture()
    
    currentImage = Path(CURRENT_IMAGE)
    oldImage = Path(OLD_IMAGE)
    Util.log("Comparing images")
    if oldImage.is_file():
        try:
            isAvailable = pooltableChecker.isTableFree(CURRENT_IMAGE, OLD_IMAGE)
        except Exception as e:
            Util.log(str(e))
    if isAvailable != wasAvailable:
        Util.log('Printing availability: ', str(isAvailable))
        mattermost_client.updateMattermostAvailable(isAvailable)
    
    wasAvailable = isAvailable
    
    currentImage.rename("old.jpg")

while True:
    CommandHandler.updateSettings()
    checkAvailability()
    time.sleep(CommandHandler.getInterval())
