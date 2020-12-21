import numpy as np
import cv2
from cv2 import aruco
from augment import four_point_transform
from augment import augment


flatten = lambda l: [item for sublist in l for item in sublist]

aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)
parameters = aruco.DetectorParametrs_create()

corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict,\
                                                      parameters=parameters)


# assignment (need a way to type)
# variable marker comes onto screen and student can type
# variable name
ids2 = ids.flatten()

class Marker(object):
    def __init__(self, label):
        self.label = label
      
        

    def display(self, video_frame, image):
        augment(self.label, frame, corners, (width, height), video_frame,\
                (frame_width, frame_height), image)


class Variable(Marker):
    def __init__(self):
        Marker.__init__(self, 0)
        self.name = input("Please enter a name for the variable: ")
        self.value = input("Please enter a value for the variable: ")

    def display(self):
        blank = np.zeros((200, 200, 3), np.uint8)
        blank_image[:, 0:200/2] = (255, 255, 255)

        font = cv2.FONT_HERSHEY_SIMPLEX
        bc = (10, 500)
        text = self.name + " = " + self.value

        
        cv2.putText(blank_image, text, bc, cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0),\
                    2)
        
        Marker.display(blank_image, frame)

    def print(self):
        print(self.name, ":", self.value)
    

    
    
