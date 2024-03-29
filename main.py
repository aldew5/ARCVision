import tkinter as tk
from PIL import Image
from PIL import ImageTk
import threading
import cv2
from cv2 import aruco
from source.utils.frames import get_frames
from tkinter import scrolledtext
from source.markers import *
import keyboard

cap = cv2.VideoCapture(0)

aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)
parameters = aruco.DetectorParameters_create()

# store a dictionary of detected markers outside the main loop
# so we can store their values 
detected = {}

# initialize the dictionary
for i in range(50):
    detected[i] = False

# keep lists of different markers
variables = {}
operators = {}
loops = {}

# keep track of whether or not an operation has been performed
# and set a timer between them
timeout = 0
updated = False

class Console():
    def __init__(self, x, y, window):
        self.x = x
        self.y = y
        self.cursor = '> '
        self.window = window

        self.textfield = scrolledtext.ScrolledText(self.window,  
                                      wrap = tk.WORD,  
                                      width = 30,  
                                      height = 27,  
                                      font = ("Times New Roman", 
                                              15))
  
    def show(self):
        """Displays console"""
        self.textfield.place(relx=self.x, rely=self.y)
    
    def update(self, text):
        """Updates console text"""
        self.textfield.insert(tk.INSERT,  "\n" + text)

    def get_text(self):
        """Retrieves console text"""
        a = self.textfield.get('1.0', 'end-1c')
        return a

    def get_input(self, text):
        """Retrieves user input"""
        self.textfield.delete('1.0', 'end')
        self.update(text)
        # must then wait for enter key to be pressed
        while True:
            if keyboard.is_pressed('enter'):
                break
            
        val = self.get_text()
        ind = len(text) + 1

        self.textfield.delete('1.0', 'end')
       
        return val[ind:]
    

class Menu(tk.Frame):
    def __init__(self, window):
        self.window = window

    def show(self):
        """Displays menu"""
        title = tk.Label(self.window, text="ARCVision",
                         anchor="center",
                         font=("Times New Roman", 20))
        title.place(relx=0.35, rely=0.3)

        checked = tk.IntVar()
        box = tk.Checkbutton(self.window, text="Enable descriptors", variable=checked)
        box.place(relx=0.35, rely=0.4)

        start = tk.Button(self.window,
                          text="Start Application",
                          command=self.destroy,
                          bg="green")
        start.place(relx=0.35, rely=0.5)

    def destroy(self):
        """Destorys introductory menu"""
        self.window.destroy()
    
        
class App():
    def __init__(self, window, vs):
        self.window = window
        self.vs = vs
        self.frames = []
        self.thread = None
        self.stopEvent = None
        self.panel1 = None
        self.panel2 = None
        self.console = Console(0.6, 0.15, self.window)
        
        self.stopEvent = threading.Event()
        self.thread = threading.Thread(target=self.videoLoop, args=())
        self.thread.start()

    def show(self):
        """Dislpays app"""
        title = tk.Label(self.window, text="ARCVision",
                         anchor="center",
                         font=("Times New Roman", 20))
        title.place(relx=0.4, rely=0.05)
        subtitle = tk.Label(self.window, text="Commands",
                            font=("Time New Roman", 15))
        subtitle.place(relx=0.65, rely=0.1)

        self.console.show()
        

    def videoLoop(self):
        """
            Main video loop that generates and augments
            the two threads that will be displayed in the
            panels
        """
        try:
            while not self.stopEvent.is_set():
                self.frames = get_frames(self.vs, aruco_dict, parameters, detected,
                                         variables, operators, loops, timeout, updated, self.console)
                self.frames[0] = cv2.resize(self.frames[0], (300,300))
                self.frames[1] = cv2.resize(self.frames[1], (300,300))

                # swap the channels becuase openCV uses BGR whereas PIL
                # uses RGB
                image1 = cv2.cvtColor(self.frames[0], cv2.COLOR_BGR2RGB)
                image1 = Image.fromarray(image1)
                image1 = ImageTk.PhotoImage(image1)
            
                image2 = cv2.cvtColor(self.frames[1], cv2.COLOR_BGR2RGB)
                image2 = Image.fromarray(image2)
                image2 = ImageTk.PhotoImage(image2)

                # create the panel
                if self.panel1 is None:
                    self.panel1 = tk.Label(image=image1)
                    self.panel1.image = image1
                    self.panel1.place(relx=0.05, rely=0.15)

                else:
                    # update the panel
                    self.panel1.configure(image=image1)
                    self.panel1.image = image1
                
                if self.panel2 is None:
                    self.panel2 = tk.Label(image=image2)
                    self.panel2.image = image2
                    self.panel2.place(relx=0.05, rely=0.55)
                else:
                    self.panel2.configure(image=image2)
                    self.panel2.image = image2

        except RuntimeError:
            print("[INFO] caught a RuntimeError")
      

# run from the same file
if (__name__ == "__main__"):
    window = tk.Tk()
    window.title("ARCVision")
    window.geometry("500x500")
    
    menu = Menu(window)
    menu.show()
    menu.window.mainloop()

    # new window
    window = tk.Tk()

    window.title("ARCVision")
    window.geometry("800x800")
    
    app = App(window, cap)
    
    app.show()
    app.window.mainloop()
