import numpy as np
import cv2
from cv2 import aruco
from augment import *


class Marker(object):
    """
    An abstract class that defines some methods all markers in the program
    will use
    """
    def __init__(self, id, eindex, image, frame, corners, frame_width, frame_height):
        self.id = id
        self.eindex = eindex
        self.frame = frame
        self.image = image
        self.corners = corners
        self.width, self.height = 200, 200
        self.frame_width, self.frame_height = frame_width, frame_height
        
    # must be updated for each new frame
    def update(self, eindex, image, frame, corners):
        self.eindex = eindex
        self.image = image
        self.frame = frame
        self.corners = corners  
        
    # augments the ArUco Marker
    def display(self, video_frame, image):
        augment(self.eindex, self.frame, self.corners, (self.width, self.height), video_frame,\
                (self.frame_width, self.frame_height), image)


class Variable(Marker):
    """ Variable class """
    
    def __init__(self, id, image, eindex, frame, corners, frame_width, frame_height):
        Marker.__init__(self, id, eindex, image, frame, corners, frame_width, frame_height)

        # take user input for variable declaration
        self.type = input("Please declare the variable's type (String or Int): ")
        self.name = input("Please enter a name for the variable: ")
        self.value = input("Please enter a value for the variable: ")
        
        if self.type == "String" or self.type == "string":
            self.type = "string"
        elif self.type == "Int" or self.type == "int":
            self.type = "int"

        # not a valid type
        else:
            print("ERROR")
            print(self.type, "is not a valid variable type")

            loop = True
            # ask the user to input a valid type until they do so
            while loop:
                self.type = input("Please input a new type: ")

                if self.type != "string" and self.type != "String" and self.type != "Int" and self.type != "int":
                    print("ERROR")
                    print(self.type, "is an invalid varaible type")
                else:
                    loop = False
            

        if self.type == "int":
            try:
                self.value = int(self.value)
            # self.value couldn't be converted to an integer
            # the input value was invalid
            except TypeError:
                print("ERROR")
                print("The value assigned to", self.name, "doesn't match the type")

                loop = True
                # request that the user input a valid number
                # until they do so
                while True:
                    try:
                        self.value = int(input("Please input a new value: "))
                        loop = False
                    except ValueError:
                        print("ERROR")
                        print("The value assigned to", self.name, "doesn't match the type")
                        loop = True
                    if not loop:
                        break
        

    def display(self):
        # blank frame
        blank = np.zeros((200, 200, 3), np.uint8)
        # set it to white
        blank[:, 0:200] = (255, 255, 255)

        # write the variable text on the marker
        font = cv2.FONT_HERSHEY_SIMPLEX
        bc = (10, 100)
        text = self.name + " = " + str(self.value)

        # put the text in the frame
        cv2.putText(blank, text, bc, cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0),\
                    2)

        # create the frame and display it
        blank_frame = cv2.resize(blank, (200, 200))
        
        Marker.display(self, blank_frame, self.image)
        
        

    def print(self):
        """ Neat printing format """
        print(self.name, ":", self.value)
        
    def set_value(self, value):
        """ Setter for value """
        self.value = value 
    
    
    

class Operator(Marker):
    """
    Operators are responsible for initiating operations between
    variables, or a variable and a value
    """
    
    def __init__(self, id, image, eindex, frame, corners, frame_width, frame_height):
        Marker.__init__(self, id, eindex, image, frame, corners, frame_width, frame_height)
        self.oper = input("What operation would you like to perform: ")
    
    def display(self):
        blank = np.zeros((200, 200, 3), np.uint8)
        blank[:, 0:200] = (255, 255, 255)

        font = cv2.FONT_HERSHEY_SIMPLEX
        bc = (100, 100)
        
        cv2.putText(blank, self.oper, bc, cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0),\
                    2)
        
        blank_frame = cv2.resize(blank, (200, 200))
        
        Marker.display(self, blank_frame, self.image)
        
    def compute(self, var1, var2=None, value=None):
        """ Carry out an operation """

        # it is a value, variable operation
        if (var2 == None):
            # make sure the value given is compatible with numerical operations
            if (var1.type == "num" and (type(value) == int or type(value) == float)):
                if (self.oper == '+'):
                    var1.set_value(var1.value + value)
                elif (self.oper == '-'):
                    var1.set_value(var1.value - value)
                elif (self.oper == '*'):
                    var1.set_value(var1.value * value)
                elif (self.oper == '/'):
                    var1.set_value(var1.value / value)

            # make sure the value is concatenable with a string
            elif (var1.type == "string" and type(value) == str):
                if (self.oper == '+'):
                    var1.set_value(var1.value + value)
                else:
                    print("ERROR")
                    print("The", self.oper, "operation is undefined for objects of type string")
            else:
                print("ERROR")
                print("Incompatible data types")

        # variable, variable operation
        elif(value == None):
            # the variables must have the same type
            if (var1.type == var2.type):
                # complete the operation
                if (self.oper == '+'):
                    var1.set_value(var1.value + var2.value)
                # not a concatenation operation and the type isn't a string
                elif (var1.type == "string"):
                    print("ERROR")
                    print("The", self.oper, "operation is undefined for objects of type string")
                elif (self.oper == '-'):
                    var1.set_value(var1.value - var2.value)
                elif (self.oper == '*'):
                    var1.set_value(var1.value * var2.value)
                elif (self.oper == '/'):
                    var1.set_value(var1.value / var2.value)
                    
            else:
                print("ERROR")
                print("Incompatible data types")
        
class Loop(Marker):
    def __init__(self, id, image, eindex, frame, corners, frame_width, frame_height, iter_count):
        Marker.__init__(self, id, eindex, image, frame, corners, frame_width, frame_height)
        self.iter_count = iter_count

        # need a way of storing updates
        # the start marker opens a terminal
        # the user can type in python code (maybe some sort of aid?)
        # then when they confirm, the program will be run self.iter_count times

    def run():
        pass
    
    
            
        
        
    
