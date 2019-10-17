from ImageComparator import ImageComparator
from ImageHandler import ImageHandler
from PoolTableFinder import PoolTableFinder
import Logger
import numpy

class PoolTableChecker:

    def __init__(self):
        self.tableFinder = PoolTableFinder()
        self.imageComparator = ImageComparator()
        self.imageHandler = ImageHandler()

    def isTableFree(self, imagePathA, imagePathB):
        imageA = self.imageHandler.readImage(imagePathA)
        imageB = self.imageHandler.readImage(imagePathB)

        tableABounds = self.tableFinder.getBoundingRectForTable(imageA)
        tableBBounds = self.tableFinder.getBoundingRectForTable(imageB)
        
        largestBounds = self.imageHandler.getLargestBoundingRect(tableABounds, tableBBounds)

        croppedA = self.imageHandler.cropImageByBoundingRect(imageA, largestBounds)
        croppedB = self.imageHandler.cropImageByBoundingRect(imageB, largestBounds)

        return self.imageComparator.areImagesEqual(croppedA, croppedB)

