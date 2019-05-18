#program to filter out the colours of the track using a 'dummy image'
#and draw contours

import cv2
import numpy as np

def nothing(x):
    pass

#dummy track image
img = cv2.imread('dummy track.png')

#create the trackbar window
window = np.zeros((300,512,3), np.uint8)
cv2.namedWindow('window')

#create trackbars for lower hsv
cv2.createTrackbar('l_H','window',0,255,nothing)
cv2.createTrackbar('l_S','window',0,255,nothing)
cv2.createTrackbar('l_V','window',0,255,nothing)

#create trackbars for upper hsv
cv2.createTrackbar('u_H','window',0,255,nothing)
cv2.createTrackbar('u_S','window',0,255,nothing)
cv2.createTrackbar('u_V','window',0,255,nothing)

while(True):
    #converting image to hsv color space
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    #creating an array for lower range hsv values
    lh = cv2.getTrackbarPos('l_H','window')
    ls = cv2.getTrackbarPos('l_S','window')
    lv = cv2.getTrackbarPos('l_V','window')
    lower = np.array([lh,ls,lv])

    #creating an array for upper range hsv values
    uh = cv2.getTrackbarPos('u_H','window')
    us = cv2.getTrackbarPos('u_S','window')
    uv = cv2.getTrackbarPos('u_V','window')
    upper = np.array([uh,us,uv])

    mask = cv2.inRange(hsv, lower, upper)
    res = cv2.bitwise_and(hsv, hsv, mask = mask)

    #applying and drawing contours
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    for contour in contours:
        cv2.drawContours(img, contour, -1, (0, 255, 0), 3)

    cv2.imshow("img",img)
    cv2.imshow("mask",mask)

    if cv2.waitKey(1) & 0xFF == ord('q'):
       break

cv2.destroyAllWindows()


    
    
    
    
