from markers import Marker
import cv2
from cv2 import aruco
from augment import *
from subprocess import call
from loop_code import run

class Loop(Marker):
    def __init__(self, id, image, eindex, frame, corners, frame_width, frame_height, iter_count):
        Marker.__init__(self, id, eindex, image, frame, corners, frame_width, frame_height)
        self.iter_count = iter_count
        self.lines = []

    def set_code(self):
        file = open("loop_code.py", 'w')
        
        print("Write the loop code here: ")
    
        while True:
            line = input()
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
        for i in range(self.iter_count):
            run()


        
