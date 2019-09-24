from ImageComparator import ImageComparator
from ImageHandler import ImageHandler
from PoolTableFinder import PoolTableFinder

class PoolTableChecker:

    def __init__(self):
        self.tableFinder = PoolTableFinder()
        self.imageComparator = ImageComparator()
        self.imageHandler = ImageHandler()

    def isTableFree(self, imagePathA, imagePathB):
        imageA = self.imageHandler.readImage(imagePathA)
        imageB = self.imageHandler.readImage(imagePathB)

        tableRect = self.tableFinder.getBoundingRectForPoolTable(imageA)

        croppedA = self.imageHandler.cropImage(imageA, tableRect)
        croppedB = self.imageHandler.cropImage(imageB, tableRect)

        return self.imageComparator.areImagesEqual(croppedA, croppedB)

