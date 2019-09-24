
from skimage.measure import compare_ssim
import cv2 as cv
import CommandHandler

class ImageComparator:        

    def areImagesEqual(self, imageA, imageB):
        self.equalityThreshold = CommandHandler.getSensitivity()
        
        grayA = self.getGrayscale(imageA)
        grayB = self.getGrayscale(imageB)

        score = self.calculateEqualityScore(grayA, grayB)
        return score > (1-self.equalityThreshold)

    def getGrayscale(self, image):
        return cv.cvtColor(image, cv.COLOR_BGR2GRAY)

    def calculateEqualityScore(self, grayA, grayB):
        (score, diff) = compare_ssim(grayA, grayB, full=True)
        return score
