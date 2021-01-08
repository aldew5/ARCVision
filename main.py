import numpy as np
import cv2
from cv2 import aruco
from augment import *
from markers import *
from distance import distance
from color_detection import detect_color


# access webcame video stream
cap = cv2.VideoCapture(0)
# delare the aruco dictionary
aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)
parameters = aruco.DetectorParameters_create()

# store a dictionary of detected markers outside the main loop
# so we can store their values 
detected = {}

# inintialize the dictionary
for i in range(50):
    detected[i] = False

# keep lists of different markers
variables = {}
operators = {}

# keep track of whether or not an operation has been performed
# and set a timer between them
timeout = 0
updated = False


while (cap.isOpened()):
    # capture frame by frame
    ret, frame = cap.read()
    # take the dimensions of the image
    frame_height, frame_width, frame_channels = frame.shape

    # covert to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # detect the markers and frame them
    corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict,\
                                                      parameters=parameters)
    frame_markers = aruco.drawDetectedMarkers(frame.copy(), corners, ids)
    img1 = frame

    # keep a list of the variables and operators currently
    # in the frame
    curvar, curops = [], []
    
    # we have detected at least one marker
    if (len(corners)):
        # create a 1D array of the markers 
        ids2 = ids.flatten()
        
        eindex = -1
        for id in ids2:
            # save the index in the corners array
            # that corresponds to the current id
            eindex += 1
            
            if (id == 2):
                # declare a new operator
                if (not detected[id]):
                    oper = Operator(id, img1, eindex, frame, corners, frame_width, frame_height)
                    operators[id] = oper
                # update the curops array
                curops.append(operators[id])
            else:
                # delcare a new varaible 
                if (not detected[id]):
                    var = Variable(id, img1, eindex, frame, corners, frame_width, frame_height)
                    variables[id] = var
                curvar.append(variables[id])
            detected[id] = True
        

        # loop through the variables currently in the frame
        for var in curvar:
           
            eindex = -1
            for id in ids2:
                eindex += 1
                # update them with the current parameters
                if (id == var.id):
                    var.update(eindex, img1, frame, corners)
            # augment
            var.display()

        # udpate the operators in the frame and display them
        for oper in curops:
            eindex = -1
            for id in ids2:
                eindex += 1
                if (id == oper.id):
                    oper.update(eindex, img1, frame, corners)
            oper.display()
            
            
        # check for operation
        if (len(curops) and len(curvar) and not updated):
            # confirm the operation with a red object in the frame
            if (detect_color(frame, "red")):
                # keep track of variables used in operations
                # (for multi-variable operations)
                completed = {}
                for i in range(50):
                    completed[i] = False
                    
                # 2D list of valid operator variable pairs
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
                        
                        # compute the distance between the varaible and the
                        # marker 
                        d = distance(tl, tr, br, bl, tl2, tr2, br2, bl2)

                        # if they are close enough add them as a possible
                        # operation to the poss array
                        if (d <= 300):
                            poss.append([var, op])
                            updated = True
                
                # multi-variable operation
                for i in poss:
                    for j in poss:
                        # make sure the varaibles are different and the operators
                        # are the same
                        if (i[0].id != j[0].id and i[1].id == j[1].id):
                            completed[i[0].id] = True
                            completed[j[0].id] = True
                            op.compute(i[0], var2=j[0])
                
                # single variable operations
                for i in poss:
                    if (not completed[i[0].id]):
                        # request the value that will be used in the computation
                        value = input("Please input a value to update " + var.name + " : ")

                        # numerical computation
                        if (var.type == "num"):
                            value = int(value)
                                
                        op.compute(var, value=value)
                
                        
                        
                        
                        
        
    # show the different frames
    cv2.imshow("augmented", img1)
    cv2.imshow("Frame Markers", frame_markers)

    # we completed an operation so update the timeout counter
    if (updated):
        timeout += 1

    # if we reach timeout == 50, we can perform another operation
    if (timeout == 50):
        updated = False
    
    # if we quite
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
# close the frames
cap.release()
cv2.destroyAllWindows()

