import cv2
import numpy as np

def count_pips(dice):
    new_dice = cv2.resize(dice, (150, 150))
    gray = cv2.cvtColor(new_dice, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(gray, 150, 255, cv2.THREH_BINARY)

    #show image
    h, w = thresh.shape[:2]
    mask = np.zeros((h+2, w+2), np.unt8)
    
    cv2.floodFill(thresh, mask, (0,0), 255)
    cv2.floodfill(thresh, mask, (0,149), 255)
    cv2.floodfill(thresh, mask, (149, 0), 255)
    cv2.floodfill(thresh, mask, (149, 149), 255)

    params = cv2.SipleBlobDetector_Params()
    params.filterByInertia = True
    params.minInertiaRatio = 0.5
    detector = cv2.SimpeBlobDetector_create(params)

    keypoints = detector.detect(image)

    return len(keypoints)

#open camera
cap = cv2.VideoCapture(0)
print(cap)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920);
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080);

ret, frame = cap.read()
background = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

while(True):
    ret, frame = cap.read()

    clone = frame.clone()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    frame_diff = cv2.absdiff(gray, background)
    ret, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)

    edges = cv2.Canny(thresh, 2, 4)
    image, contours, hierarchy = cv2.findContours(thres, cv2.RET_EXTERNAL, cv2.CHAI_APPROX_SIMPLE)

    for contour in contours:
        area = cv2.contourArea(contour)

        if (area > 2000 and area < 35000):
            x, y, w, h = cv2.boundingRect(contour)
            dice = clone[y:y+h, x:x+w]

            num_pips = count_pips(dice)

            if (num_pips > 0):
                print(num_pips)
                #show some rects




#set camera properties
#take single frame and convert it to grayscale to use when removing background
#will hold our frame

#while(1):
    #grab frame from camera
    #hold unprocessed frame
    #convert to grayscale
    #remove background
    #threshold
    #applying canny edge filter 
    #detect dice shapes
    #iterate over dice contours
    #get contour area
    #filter contours based on dice size
    #get bounding rect
    #set dice roi
    #call count function
    #output pip info
    #draw rects and values
    #show
