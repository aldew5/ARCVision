from markers import Marker
import cv2
from cv2 import aruco
from augment import *
from loop import Loop

loop = Loop(5, 5, 5, 5, 5, 5, 5, 5)
loop.set_code()
loop.execute()
