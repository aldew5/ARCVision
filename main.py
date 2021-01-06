import numpy as np
import cv2
from cv2 import aruco
from augment import *
from markers import *
from distance import distance
from color_detection import detect_red


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
        
        eindex = -1
        for id in ids2:
            eindex += 1
            
            if (id == 2):
                if (not detected[id]):
                    oper = Operator(id, img1, eindex, frame, corners, frame_width, frame_height)
                    operators[id] = oper
                curops.append(operators[id])
            else:
                if (not detected[id]):
                    var = Variable(id, img1, eindex, frame, corners, frame_width, frame_height)
                    variables[id] = var
                curvar.append(variables[id])
            detected[id] = True
        
      
        for var in curvar:
           
            eindex = -1
            for id in ids2:
                eindex += 1
                if (id == var.id):
                    var.update(eindex, img1, frame, corners)
            var.display()
            
        for oper in curops:
            eindex = -1
            for id in ids2:
                eindex += 1
                if (id == oper.id):
                    oper.update(eindex, img1, frame, corners)
            oper.display()
            
            
        # check for operation
        if (len(curops) and len(curvar) and not updated):
            if (detect_red(frame)):
                # keep track of variables used in operations
                completed = {}
                for i in range(50):
                    completed[i] = False
                    
                # 2D list of valid operator varaible pairs
                poss = []
                # support single variable operations
                for op in curops:  
                    tl = corners[op.eindex][0][0]
                    tr = corners[op.eindex][0][1]
                    br = corners[op.eindex][0][2]
                    bl = corners[op.eindex][0][3]
        
                        
                    for var in curvar:
                        tl2 = corners[var.eindex][0][0]
                        tr2 = corners[var.eindex][0][1]
                        br2 = corners[var.eindex][0][2]
                        bl2 = corners[var.eindex][0][3]
                        
                        d = distance(tl, tr, br, bl, tl2, tr2, br2, bl2)
                        print(d, var.id)
                        
                        if (d <= 300):
                            poss.append([var, op])
                            updated = True
                
                
                for i in poss:
                    for j in poss:
                        # multi-variable operation
                        if (i[0].id != j[0].id and i[1].id == j[1].id):
                            completed[i[0].id] = True
                            completed[j[0].id] = True
                            op.compute(i[0], var2=j[0])
                
                # single variable operations
                for i in poss:
                    if (not completed[i[0].id]):
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

