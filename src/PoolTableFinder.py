import numpy
import cv2 as cv
import CommandHandler
import ConfigHandler
import Logger
from ImageHandler import ImageHandler

from exception.PoolTableException import PoolTableException


class PoolTableFinder:
    
    def __init__(self):
        self.imageHandler = ImageHandler()
        self.currentImagePath = ConfigHandler.getCurrentImagePath()
        self.croppedImagePath = ConfigHandler.getCroppedImagePath()
    
    def saveCroppedImage(self):
        Logger.info("Saving cropped image")
        
        currentImage = self.imageHandler.readImage(self.currentImagePath)
        if CommandHandler.areBoundsSet():
            bounds = CommandHandler.getBounds()
            croppedImage = self.imageHandler.cropAndRotateRectangleInImage(currentImage, bounds)
        else:
            bounds = self.getBoundingRectForTable(currentImage)
            croppedImage = self.imageHandler.cropImageByBoundingRect(currentImage, bounds)

        cv.imwrite(self.croppedImagePath, croppedImage)

    def getMaskForTable(self, poolImage):
        self.th_green_low = numpy.array(CommandHandler.getThGreenLow())
        self.th_green_high = numpy.array(CommandHandler.getThGreenHigh())
        
        hsvImage = cv.cvtColor(poolImage, cv.COLOR_BGR2HSV)
        return self.getMask(hsvImage)
        
    def getBoundingRectForTable(self, poolImage):
        mask = self.getMaskForTable(poolImage)
        contours = self.getContours(mask)
        return self.getLargestBoundingRect(contours)

    def getMask(self, hsvImage):
        mask = cv.inRange(hsvImage, self.th_green_low, self.th_green_high)

        return mask

    def getContours(self, mask):
        contours = cv.findContours(mask.copy(),
                                   cv.RETR_EXTERNAL,
                                   cv.CHAIN_APPROX_SIMPLE)[-2]
        if len(contours) == 0:
            raise PoolTableException("No contours found")

        return contours

    def getLargestBoundingRect(self, contours):
        area = max(contours, key=cv.contourArea)
        return cv.boundingRect(area)
