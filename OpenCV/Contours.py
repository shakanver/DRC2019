import cv2
import numpy as np

cap = cv2.VideoCapture(0)

while True:
    _, frame = cap.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)


    lower_red = np.array([10, 50, 50])
    upper_red = np.array([255,255,180])

    #the mask specifies the range of colours that we want to filter out
    mask = cv2.inRange(hsv, lower_red, upper_red)
    #any colors in range will be shown as they are on the frame
    res = cv2.bitwise_and(frame, frame, mask = mask)


    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    for contour in contours:
        cv2.drawContours(frame, contour, -1, (0, 255, 0), 3)

    cv2.imshow("frame",frame)
    cv2.imshow("mask",mask)

    if cv2.waitKey(1) & 0xFF == ord('q'):
       break

cv2.destroyAllWindows()
cap.release()
