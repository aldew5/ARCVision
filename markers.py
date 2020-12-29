import numpy as np
import cv2
from cv2 import aruco
from augment import four_point_transform
from augment import augment



# variable marker comes onto screen and student can type
# variable name

class Marker(object):
    def __init__(self, label, image, frame, corners, frame_width, frame_height):
        self.label = label
        self.frame = frame
        self.image = image
        self.corners = corners
        self.width, self.height = 200, 200
        self.frame_width, self.frame_height = frame_width, frame_height
        
    
    def update(self, image, frame, corners):
        self.image = image
        self.frame = frame
        self.corners = corners  
        

    def display(self, video_frame, image):
        augment(self.label, self.frame, self.corners, (self.width, self.height), video_frame,\
                (self.frame_width, self.frame_height), image)


class Variable(Marker):
    def __init__(self, image, label, frame, corners, frame_width, frame_height):
        Marker.__init__(self, label, image, frame, corners, frame_width, frame_height)
        
        self.name = "TEST" #input("Please enter a name for the variable: ")
        self.value = 7 #input("Please enter a value for the variable: ")
        
        if (type(self.value) == int or type(self.value) == float):
            self.type = "num"
        else if (type(self.value) == str):
            self.type = "string"
        
        

    def display(self):
        blank = np.zeros((200, 200, 3), np.uint8)
        blank[:, 0:200] = (255, 255, 255)

        font = cv2.FONT_HERSHEY_SIMPLEX
        bc = (10, 100)
        text = self.name + " = " + str(self.value)

        
        cv2.putText(blank, text, bc, cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0),\
                    2)
        
        blank_frame = cv2.resize(blank, (200, 200))
        
        Marker.display(self, blank_frame, self.image)
        
        

    def print(self):
        print(self.name, ":", self.value)
    
    
    

class Operator(Marker):
    def __init__(self, image, label, frame, corners, frame_width, frame_height):
        Marker.__init__(self, label, image, frame, corners, frame_width, frame_height)
        self.oper = '+' #input("What operation would you like to perform: ")
    
    def display(self):
        blank = np.zeros((200, 200, 3), np.uint8)
        blank[:, 0:200] = (255, 255, 255)

        font = cv2.FONT_HERSHEY_SIMPLEX
        bc = (10, 100)
        
        cv2.putText(blank, self.oper, bc, cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0),\
                    2)
        
        blank_frame = cv2.resize(blank, (200, 200))
        
        Marker.display(self, blank_frame, self.image)
        
    def compute(self, var1, var2=None, value=None):
        if (var2 == None):
            if (var1.type == "num" and (type(value) == int or type(value) == float)):
                var1.value += value
            else if (var1.type == "string" and type(value) == str):
                var1.value += value
            else:
                print("ERROR")
                print("Incompatible data types")
        
        else if (value == None):
            if (var1.type == var2.type):
                var1.value += var2.value
            else:
                print("ERROR")
                print("Incompatible data types")
        
class Loop(Marker):
    def __init__(self, image, label, frame, corners, frame_width, frame_height, iter_count):
        Marker.__init__(self, label, image, frame, corners, frame_width, frame_height)
        self.iter_count = iter_count
    
    
            
        
        
    
