import cv2 as cv

class ImageHandler:

    def readImage(self, path):
        return cv.imread(path)

    def cropImage(self, image, boundingRect):
        (x,y,w,h) = boundingRect
        return image[y:y+h, x:x+w]