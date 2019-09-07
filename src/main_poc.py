# import the necessary packages
from skimage.measure import compare_ssim
import argparse
import imutils
import cv2
import numpy

imgPath1 = "../testData/pool1.jpg"
imgPath2 = "../testData/pool1.jpg"

# load the two input images
imageA = cv2.imread(imgPath1)
imageB = cv2.imread(imgPath2)

# convert the images to grayscale
grayA = cv2.cvtColor(imageA, cv2.COLOR_BGR2GRAY)
grayB = cv2.cvtColor(imageB, cv2.COLOR_BGR2GRAY)

# compute the Structural Similarity Index (SSIM) between the two
# images, ensuring that the difference image is returned
(score, diff) = compare_ssim(grayA, grayB, full=True)
diff = (diff * 255).astype("uint8")
print("SSIM: {}".format(score))

ret,thresh = cv2.threshold(grayA,127,255,0)
cnts,hierarchy = cv2.findContours(thresh, 1, 2)


maxRect = {"w":0,"h":0,"x":0,"y":0}
for c in cnts:
    # compute the bounding box of the contour and then draw the
    # bounding box on both input images to represent where the two
    # images differ
    (x, y, w, h) = cv2.boundingRect(c)
    if w > maxRect['w'] and h > maxRect['h']:
        maxRect = {"w":w,"h":h,"x":x,"y":y}

x = maxRect['x']
y = maxRect['y']
h = maxRect['h']
w = maxRect['w']

# cv2.rectangle(imageA, (x, y), (x + w, y + h), (0, 0, 255), 2)

cv2.imshow("Img1", imageA)
# cv2.waitKey(5)

# Convert BGR to HSV
hsv = cv2.cvtColor(imageA, cv2.COLOR_BGR2HSV)
# define range of blue color in HSV
lower_blue = numpy.array([30,100,100])
upper_blue = numpy.array([90,255,255])
# Threshold the HSV image to get only blue colors
mask = cv2.inRange (hsv, lower_blue, upper_blue)
bluecnts = cv2.findContours(mask.copy(),
                            cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)[-2]

if len(bluecnts)>0:
    blue_area = max(bluecnts, key=cv2.contourArea)
    (xg,yg,wg,hg) = cv2.boundingRect(blue_area)
    cv2.rectangle(imageA,(xg,yg),(xg+wg, yg+hg),(0,255,0),2)

cv2.imshow('frame',imageA)
cv2.imshow('mask',mask)

cv2.waitKey(0)
