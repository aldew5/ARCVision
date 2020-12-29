import numpy as np
import cv2
from cv2 import aruco
from augment import four_point_transform
from augment import augment
from markers import Variable
from markers import Operator


flatten = lambda l: [item for sublist in l for item in sublist]

cap = cv2.VideoCapture(-1)

aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)
parameters = aruco.DetectorParameters_create()

rect = np.zeros((4, 2), dtype="float32")
detected = {}

for i in range(50):
    detected[i] = False

variables = []
operators = []


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
        #augment(0, frame, corners, (200, 200), blank_frame,\
                        #(frame_width, frame_height), img1)
        
        label = -1
        for id in ids2:
            label += 1
            if (not detected[id]):
                if (id == 2):
                    oper = Operator(img1, label, frame, corners, frame_width, frame_height)
                    operators.append(oper)
                else:
                    #print("label is ", label)
                    var = Variable(img1, label, frame, corners, frame_width, frame_height)
                    variables.append(var)
                detected[id] = True
        #variables[0].print()
                
        for var in variables:
            print(len(variables))
            var.update(img1, frame, corners)
            var.display()
            
        for oper in operators:
            #print("OPERATORS", len(operators))
            oper.update(img1, frame, corners)
            oper.display()
        
        
    cv2.imshow("augmented", img1)
    cv2.imshow("Frame Markers", frame_markers)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
cap.release()
cv2.destroyAllWindows()

