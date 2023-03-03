import cv2 as cv
import numpy as np
'''backSub = cv.createBackgroundSubtractorKNN()
#backSub = cv.createBackgroundSubtractorMOG2()
frame = cv.imread('./esempio_remove_background.jpg')
fgMask = backSub.apply(frame)
# reduce some noise in the fgMask
kernel = np.ones((3,3), np.uint8)
fgMask = cv.erode(fgMask,kernel,iterations=2)
fgMask = cv.dilate(fgMask,kernel,iterations=2)

fgMask[np.abs(fgMask)<250]=0

cv.imshow('Frame', frame)
cv.imshow('FGMask', fgMask)
cv.waitKey(0)'''
def resize(dst,img):
    width = img.shape[1]
    height = img.shape[0]
    dim = (width,height)
    resized = cv.resize(dst,dim,interpolation=cv.INTER_AREA)
    return resized

frame = cv.imread('./esempio_remove_background.jpg')
takeBGImage = 0

