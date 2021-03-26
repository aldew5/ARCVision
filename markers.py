import numpy as np
import cv2
from cv2 import aruco
from augment import *
from loop_code import run
import time


class Marker(object):
    """
    An abstract class that defines some methods all markers in the program
    will use
    """
    def __init__(self, id, eindex, image, frame, corners, frame_width, frame_height, console):
        self.id = id
        self.eindex = eindex
        self.frame = frame
        self.image = image
        self.corners = corners
        self.width, self.height = 200, 200
        self.frame_width, self.frame_height = frame_width, frame_height
        self.console = console
        
    # must be updated for each new frame
    def update(self, eindex, image, frame, corners):
        """Update the parameters"""
        self.eindex = eindex
        self.image = image
        self.frame = frame
        self.corners = corners  
        
    # augments the ArUco Marker
    def display(self, video_frame, image):
        """Display the AR"""
        augment(self.eindex, self.frame, self.corners, (self.width, self.height), video_frame,\
                (self.frame_width, self.frame_height), image)


class Variable(Marker):
    """ Variable class """
    
    def __init__(self, id, image, eindex, frame, corners, frame_width, frame_height, console):
        Marker.__init__(self, id, eindex, image, frame, corners, frame_width, frame_height, console)

        # take user input for variable declaration
        self.type = console.get_input("Please declare the variable's type (String or Int): ")
        time.sleep(1)
        #self.console.update("HERE", self.type)
        self.name = console.get_input("Please enter a name for the variable: ")
        time.sleep(1)
        self.value = console.get_input("Please enter a value for the variable: ")
        
        if self.type == "String" or self.type == "string":
            self.type = "string"
        elif self.type == "Int" or self.type == "int":
            self.type = "int"

        # not a valid type
        else:
            self.console.update("ERROR")
            self.console.update(self.type, "is not a valid variable type")

            loop = True
            # ask the user to input a valid type until they do so
            while loop:
                self.type = input("Please input a new type: ")

                if self.type != "string" and self.type != "String" and self.type != "Int" and self.type != "int":
                    self.console.update("ERROR")
                    self.console.update(self.type, "is an invalid varaible type")
                else:
                    loop = False
            

        if self.type == "int":
            try:
                self.value = int(self.value)
            # self.value couldn't be converted to an integer
            # the input value was invalid
            except TypeError:
                self.console.update("ERROR")
                self.console.update("The value assigned to", self.name, "doesn't match the type")

                loop = True
                # request that the user input a valid number
                # until they do so
                while True:
                    try:
                        self.value = int(input("Please input a new value: "))
                        loop = False
                    except ValueError:
                        self.console.update("ERROR")
                        self.console.update("The value assigned to", self.name, "doesn't match the type")
                        loop = True
                    if not loop:
                        break
        

    def display(self):
        """Display the AR"""
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
        """ Neat print format """
        self.console.update(self.name, ":", self.value)
        
    def set_value(self, value):
        """ Setter for value """
        self.value = value 
    
    
    

class Operator(Marker):
    """
    Operators are responsible for initiating operations between
    variables, or a variable and a value
    """
    
    def __init__(self, id, image, eindex, frame, corners, frame_width, frame_height, console):
        Marker.__init__(self, id, eindex, image, frame, corners, frame_width, frame_height, console)
        self.oper = console.get_input("What operation would you like to perform: ")
    
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

        #self.console.update(var1.type, type(value))

        # it is a value, variable operation
        if (var2 == None):
            # make sure the value given is compatible with numerical operations
            if (var1.type == "int" and (type(value) == int or type(value) == float)):
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
                    self.console.update("ERROR")
                    self.console.update("The", self.oper, "operation is undefined for objects of type string")
            else:
                self.console.update("ERROR")
                self.console.update("Incompatible data types")

        # variable, variable operation
        elif(value == None):
            # the variables must have the same type
            if (var1.type == var2.type):
                # complete the operation
                if (self.oper == '+'):
                    var1.set_value(var1.value + var2.value)
                # not a concatenation operation and the type isn't a string
                elif (var1.type == "string"):
                    self.console.update("ERROR")
                    self.console.update("The", self.oper, "operation is undefined for objects of type string")
                elif (self.oper == '-'):
                    var1.set_value(var1.value - var2.value)
                elif (self.oper == '*'):
                    var1.set_value(var1.value * var2.value)
                elif (self.oper == '/'):
                    var1.set_value(var1.value / var2.value)
                    
            else:
                self.console.update("ERROR")
                self.console.update("Incompatible data types")


class Loop(Marker):
    def __init__(self, id, image, eindex, frame, corners, frame_width, frame_height, iter_count, console):
        Marker.__init__(self, id, eindex, image, frame, corners, frame_width, frame_height, console)
        self.iter_count = iter_count
        self.lines = []

    def set_code(self):
        """Set the loop code"""
        file = open("loop_code.py", 'w')
    
        while True:
            line = self.console.get_input("Write the loop code here: ")
            if line == "END":
                break
            else:
                self.lines.append(line)

        file.write("def run():\n")
        for line in self.lines:
            file.write("\t")
            file.write(line)
            file.write("\n")

        file.close()

    def execute(self):
        """Execute loop code"""
        for i in range(self.iter_count):
            run()

    def display(self):
        """Display AR view"""
        blank = np.zeros((200, 200, 3), np.uint8)
        blank[:, 0:200] = (255, 255, 255)

        font = cv2.FONT_HERSHEY_SIMPLEX
        bc = (100, 100)
        
        cv2.putText(blank, "LOOP", bc, cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0),\
                    2)
        
        blank_frame = cv2.resize(blank, (200, 200))
        
        Marker.display(self, blank_frame, self.image)
        

        
        
    
    
            
        
        
    
