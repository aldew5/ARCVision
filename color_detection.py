import numpy as np
import cv2

image = cv2.imread("_data/marker.jpg")

def detect_color(image, color):

    # convert image from BGR to HSV (hue-stauration value)
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # set ranges
    red_lower = np.array([136, 87, 111], np.uint8)
    red_upper = np.array([180, 255, 255], np.uint8)
    red_mask = cv2.inRange(hsv_image, red_lower, red_upper)

    # Morphological transform, dilation for each color and bitwise_and
    # operator between image and mask detects only a particular color

    kernal = np.ones((5, 5), "uint8")

    red_mask = cv2.dilate(red_mask, kernal)
    res_red = cv2.bitwise_and(image, image, mask=red_mask)

     # Creating contour to track red color 
    contours, hierarchy = cv2.findContours(red_mask, 
                                           cv2.RETR_TREE, 
                                           cv2.CHAIN_APPROX_SIMPLE) 
      
    for pic, contour in enumerate(contours): 
        area = cv2.contourArea(contour) 
        if(area > 300):
            
            x, y, w, h = cv2.boundingRect(contour) 
            imageFrame = cv2.rectangle(image, (x, y),  
                                       (x + w, y + h),  
                                       (0, 0, 255), 2) 
              
            cv2.putText(image, "Red Colour", (x, y), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1.0, 
                        (0, 0, 255))
            return True
    return False
    cv2.imshow("Multiple Color Detection in Real-TIme", image) 
    

#detect_color(image, "red")
