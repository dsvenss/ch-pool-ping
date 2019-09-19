from PoolTableChecker import PoolTableChecker
import mattermost_client
import camera
import time
from pathlib import Path

INTERVALL_TIME_SECONDS = 3
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
    print("comparing images")
    if oldImage.is_file():
        try:
            isAvailable = pooltableChecker.isTableFree(CURRENT_IMAGE, OLD_IMAGE)
        except Exception as e:
            print(str(e))
    if isAvailable != wasAvailable:
        print('********************************mattermost_client ' + str(isAvailable))
        mattermost_client.updateMattermostAvailable(isAvailable)
    
    wasAvailable = isAvailable
    
    currentImage.rename("old.jpg")

while True:
    checkAvailability()
    time.sleep(INTERVALL_TIME_SECONDS)
