import cv2 as cv

# https://jdhao.github.io/2019/02/23/crop_rotated_rectangle_opencv/

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

    def cropAndRotateRectangleInImage(self, img, bounds):
        rect = cv.minAreaRect(bounds)
        
        # get the parameter of the small rectangle
        center, size, angle = rect[0], rect[1], rect[2]
        center, size = tuple(map(int, center)), tuple(map(int, size))

        # get row and col num in img
        height, width = img.shape[0], img.shape[1]

        # calculate the rotation matrix
        M = cv.getRotationMatrix2D(center, angle, 1)
        # rotate the original image
        img_rot = cv.warpAffine(img, M, (width, height))

        # now rotated rectangle becomes vertical and we crop it
        img_crop = cv.getRectSubPix(img_rot, size, center)
        
        return img_crop