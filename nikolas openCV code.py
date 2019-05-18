#This is a code that applys a few technique to detect lines using colour.
#Some of the techniques used in this code include
#1. converting colour space of image to hsv
#2. applying in range function to filter colours
#3. using erosion and dilation to filter noise
#4. masking the original image with the binary image to see colours detected
#5. finding contours within the image and drawing them
#6. getting information from contours, such as finding centroid
#7. drawing on image to visualise a path

#for more information about erode/dilate
#https://docs.opencv.org/3.0-beta/doc/py_tutorials/py_imgproc/py_morphological_ops/py_morphological_ops.html

#First import our libraries, cv2 and numpy are extremely important
import cv2              #imports opencv library to get image processing functions
import numpy as np      #numpy provides lots of array related functions

#First thing we will do is load in a video to test on by creating a video capture
#object, make sure the video you want to use is in the same location as this code
#and change the name of the video file to its name, you can also use a camera if
#you want by changing the name to the number corresponding to the camera
video = cv2.VideoCapture("ObstacleTest1.avi")

#First lets check the video object could open the video, this is helpful to do as
#weird error messages will be produced if it is not opened properly
if (video.isOpened()== False): 
    print("Error opening video stream or file")

#Lets set up our values for the hsv range, unfortunately you will probobly have
#to change these values each time you change locations due to lighting. use a
#seperate code to this one to determine these values
    
#*******************Adjust these values***********************************************
hLower = 80
sLower = 35
vLower = 100
hUpper = 180
sUpper = 255
vUpper = 255
#*************************************************************************************

#Put these values into an array, this will be helpful when passing it to functions later
lowerRange = (hLower, sLower, vLower)
upperRange = (hUpper, sUpper, vUpper)

#Now the setup part of our code is done, we can move to the main while loop which loops
#until the video feed is closed or until we press q (this is added at the end of the loop)
while(video.isOpened()):
    #The first thing we want to do is read in a frame from the video
    _, frame = video.read()

    #Convert the colour space of the image from BGR to HSV, this is because
    #hsv is much better for colour filtering
    hsvFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
    #Filter the image based on if the color value falls within the hsv range we
    #specified. This will create a binary image where pixels that fall within the
    #colour range will turn white representing True and pixels that are out of the
    #range are black representing false
    colorFilter = cv2.inRange(hsvFrame, lowerRange, upperRange)

    #Looking at the filtered image, you might notice there is random small places
    #that are being detected as the colour and areas inside the colour that are not
    #We can use the erode and dilate functions to help filter out noise and smooth images
    #First we create an element to be used for these operations, the bigger the element
    #the larger the effect it will have on the image, we are just going to make a basic
    #square element by making an array of 1's, the size of this array corresponds to the
    #size of the element
    kernel = np.ones((5, 5), np.uint8)

    #using this element we can apply an erode or dilate
    #erode = cv2.erode(image, kernel), if one pixels is false in the kernel, then centre pixel is false
    #dilate = cv2.dilate(image, kernel), if one pixel is true in the kernel, then centre pixel is true
    #opening = cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel), erosion followed by dilate, removes noise
    #closing = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel), dilate followed by erosion, fills holes
    colorFilter = cv2.dilate(colorFilter, kernel)    #play around with kernel size and operations

    #Now that we have filtered out the colours into a binary image (white is true, black is false),
    #we can overlay this binary image mask on top of the original image to see what colours and parts of the
    #original image are kept.
    originalMasked = cv2.bitwise_and(frame,frame,mask = colorFilter)
    
    #With this binary image we can find the contours. Contours are the
    #outlines of the white area in our binary image and we can use these to find
    #important properties such as centroids or curvature
    
    #uncomment this if using version 2 of opencv
    #contours, _ = cv2.findContours(colorFilter, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    modifiedImg, contours, heirachy = cv2.findContours(colorFilter, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    #need to check if contours is empty before we do anything with them
    if contours:
        #only consider the biggest contour, this is helps filter out the noise
        biggestCont = max(contours, key = cv2.contourArea)
        cv2.drawContours(frame, biggestCont, -1, (0,255,0), 3)
        
        #One important thing we can find about this contour is its centroid, this can be
        #very good as for example we can tell the car to steer to the point between the
        #two lines centroids
        #first thing we do is find the moments of the centroid, moments is something to
        #do with spacial distribution
        M = cv2.moments(biggestCont)
        #calculate x position of centroid
        cX = int(M["m10"] / M["m00"])
        #calculate y position of centroid
        cY = int(M["m01"] / M["m00"])
        #draw a circle at the centroid to show where it is
        #to draw a circle use cv2.circle(image, (x, y), radius, colour, thickness)
        cv2.circle(frame, (cX, cY), 10, (0, 0, 255), -1)       
        
        #we can also draw a line from our car to the centroid and use this line to
        #represent the path we want our car to take
        #to draw a line use cv2.line(image, (x1, y1), (x2, y2), colour, thickness)
        cv2.line(frame, (640, 480), (cX, cY), (255, 0, 255), 5)
        


    #Display the images we got, these are the original image...(remember to add more)
    cv2.imshow('original image', frame) #display the original frame from video
    cv2.imshow('first filtered image', colorFilter) #display the original frame from video
    cv2.imshow('masked image', originalMasked) #display the original frame from video
    
    #This weird if statement is to make pressing q exit the loop
    if cv2.waitKey(25) & 0xFF == ord('q'):
      break    


#When the while loop finishes, we want to finish our code by release the video capture object
#and delete all windows we made
video.release()             #release the video capture object
cv2.destroyAllWindows()     #destorys all the windows
