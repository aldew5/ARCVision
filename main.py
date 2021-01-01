import numpy as np
import cv2
from cv2 import aruco
from augment import four_point_transform
from augment import augment
from markers import Variable
from markers import Operator
from distance import distance


flatten = lambda l: [item for sublist in l for item in sublist]

cap = cv2.VideoCapture(-1)

aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)
parameters = aruco.DetectorParameters_create()

rect = np.zeros((4, 2), dtype="float32")
detected = {}

for i in range(50):
    detected[i] = False

# id to marker
variables = {}
operators = {}

timeout = 0
updated = False

while (cap.isOpened()):
    ret, frame = cap.read()
    frame_height, frame_width, frame_channels = frame.shape
    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict,\
                                                      parameters=parameters)
    frame_markers = aruco.drawDetectedMarkers(frame.copy(), corners, ids)
    img1 = frame
    
    curvar, curops = [], []
    

    if (len(corners)):
        ids2 = ids.flatten()
        #augment(0, frame, corners, (200, 200), blank_frame,\
                        #(frame_width, frame_height), img1)
        
        label = -1
        for id in ids2:
            label += 1
            
            if (id == 2):
                if (not detected[id]):
                    oper = Operator(img1, label, frame, corners, frame_width, frame_height)
                    operators[id] = oper
                curops.append(operators[id])
            else:
                if (not detected[id]):
                    var = Variable(img1, label, frame, corners, frame_width, frame_height)
                    variables[id] = var
                curvar.append(variables[id])
            detected[id] = True
        #variables[0].print()
                
        for var in curvar:
            var.print()
            var.update(img1, frame, corners)
            var.display()
            
        for oper in curops:
            #print("OPERATORS", len(operators))
            oper.update(img1, frame, corners)
            oper.display()
            
            
        # check for operation
        if (len(curops) and len(curvar) and not updated):
            # support single variable operations
            for op in curops:  
                tl = corners[op.label][0][0]
                tr = corners[op.label][0][1]
                br = corners[op.label][0][2]
                bl = corners[op.label][0][3]
                    
                for var in curvar:
                    tl2 = corners[var.label][0][0]
                    tr2 = corners[var.label][0][1]
                    br2 = corners[var.label][0][2]
                    bl2 = corners[var.label][0][3]
                    
                    d = distance(tl, tr, br, bl, tl2, tr2, br2, bl2)
                    
                    if (d <= 200):
                        updated = True
                        value = input("Please input a value to update " + var.name + " : ")
                        
                        if (var.type == "num"):
                            value = int(value)
                            
                        op.compute(var, value=value)
                
                        
                        
                        
                        
        
        
    cv2.imshow("augmented", img1)
    cv2.imshow("Frame Markers", frame_markers)
    
    if (updated):
        timeout += 1
    
    if (timeout == 50):
        updated = False
    
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
cap.release()
cv2.destroyAllWindows()

