import cv2 as cv

class ImageHandler:

    def readImage(self, path):
        return cv.imread(path)
    
    def getLargestBoundingRect(self, boundsA, boundsB):
        (xA,yA,wA,hA) = boundsA
        (xB,yB,wB,hB) = boundsB
        if wA*hA > wB*hB:
            return boundsA
        
        return boundsB

    def cropImageByBoundingRect(self, image, boundingRect):
        (x,y,w,h) = boundingRect
        return image[y:y+h, x:x+w]
    
    def cropImageByMask(self, image, mask):
        return cv.bitwise_and(image,image, mask=mask)