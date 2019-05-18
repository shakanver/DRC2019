import cv2
import numpy as np

cap = cv2.VideoCapture(0)

while True:
    _, frame = cap.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)


    lower = np.array([10, 50, 50])
    upper = np.array([255,255,180])

    #the mask specifies the range of colours that we want to filter out
    mask = cv2.inRange(hsv, lower, upper)
    #any colors in range will be shown as they are on the frame
    res = cv2.bitwise_and(frame, frame, mask = mask)

    
    kernel = np.ones((5,5), np.uint8)
    erosion = cv2.erode(res, kernel, iterations = 1)
    dilation = cv2.dilate(res, kernel, iterations = 1)
    

    cv2.imshow('frame', frame)
    cv2.imshow('mask', mask)
    cv2.imshow('erosion', erosion)
    cv2.imshow('dilation', dilation)
    cv2.imshow('res', res)

    if cv2.waitKey(1) & 0xFF == ord('q'):
       break

cv2.destroyAllWindows()
cap.release()
