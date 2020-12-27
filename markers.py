import numpy as np
import cv2
from cv2 import aruco
from augment import four_point_transform
from augment import augment



# variable marker comes onto screen and student can type
# variable name

class Marker(object):
    def __init__(self, label):
        self.label = label
      
        

    def display(self, video_frame, image):
        augment(self.label, frame, corners, (width, height), video_frame,\
                (frame_width, frame_height), image)


class Variable(Marker):
    def __init__(self, image, label, frame, corners, frame_width, frame_height):
        self.label = label
        self.frame = frame
        self.image = image
        self.name = input("Please enter a name for the variable: ")
        self.value = input("Please enter a value for the variable: ")
        self.corners = corners
        self.width = 200
        self.height = 200
        self.frame_width, self.frame_height = frame_width, frame_height
        

    def display(self):
        blank = np.zeros((200, 200, 3), np.uint8)
        blank[:, 0:200] = (255, 255, 255)

        font = cv2.FONT_HERSHEY_SIMPLEX
        bc = (10, 500)
        text = self.name + " = " + self.value

        
        cv2.putText(blank, text, bc, cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0),\
                    2)
        
        blank_frame = cv2.resize(blank, (200, 200))
        
        augment(self.label, self.frame, self.corners, (self.width, self.height), blank_frame,\
                (self.frame_width, self.frame_height), self.frame)

    def print(self):
        print(self.name, ":", self.value)
    

    
    
