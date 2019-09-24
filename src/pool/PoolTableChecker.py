from image.ImageComparator import ImageComparator
from image.ImageHandler import ImageHandler
from pool.PoolTableFinder import PoolTableFinder

class PoolTableChecker:

    def __init__(self):
        self.tableFinder = PoolTableFinder()
        self.imageComparator = ImageComparator(0.02)
        self.imageHandler = ImageHandler()

    def isTableFree(self, imagePathA, imagePathB):
        imageA = self.imageHandler.readImage(imagePathA)
        imageB = self.imageHandler.readImage(imagePathB)

        tableRect = self.tableFinder.getBoundingRectForPoolTable(imageA)

        croppedA = self.imageHandler.cropImage(imageA, tableRect)
        croppedB = self.imageHandler.cropImage(imageB, tableRect)

        return self.imageComparator.areImagesEqual(croppedA, croppedB)

