import numpy as np
import cv2
from cv2 import aruco
from augment import four_point_transform
from augment import augment
from markers import Variable


flatten = lambda l: [item for sublist in l for item in sublist]

cap = cv2.VideoCapture(-1)

aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)
parameters = aruco.DetectorParameters_create()

rect = np.zeros((4, 2), dtype="float32")
detected = {}

for i in range(50):
    detected[i] = False

variables = []


while (cap.isOpened()):
    ret, frame = cap.read()
    frame_height, frame_width, frame_channels = frame.shape
    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict,\
                                                      parameters=parameters)
    frame_markers = aruco.drawDetectedMarkers(frame.copy(), corners, ids)
    img1 = frame
    

    if (len(corners)):
        ids2 = ids.flatten()
        
        label = -1
        for id in ids2:
            label += 1
            if (not detected[id]):
                print("label is ", label)
                var = Variable(img1, label, frame, corners, frame_width, frame_height)
                variables.append(var)
                detected[id] = True
                
        for var in variables:
            var.print()
            var.display()
        
        
    cv2.imshow("augmented", img1)
    cv2.imshow("Frame Markers", frame_markers)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
cap.release()
cv2.destroyAllWindows()

