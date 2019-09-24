import numpy
import cv2 as cv
import CommandHandler

from exception.PoolTableException import PoolTableException


class PoolTableFinder:

    def getBoundingRectForPoolTable(self, poolImage):
        self.th_green_low = numpy.array(CommandHandler.getThGreenLow())
        self.th_green_high = numpy.array(CommandHandler.getThGreenHigh())
        
        hsvImage = cv.cvtColor(poolImage, cv.COLOR_BGR2HSV)
        mask = self.getMask(hsvImage)
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
