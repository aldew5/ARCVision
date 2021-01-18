import tkinter as tk
from PIL import Image
from PIL import ImageTk
import threading
import datetime
import imutils
import cv2


class Menu(tk.Frame):
    def __init__(self, window):
        self.window = window

    def show(self):
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
        self.window.destroy()
        
        window = tk.Tk()
        window.title("ARCVision")
        window.geometry("500x500")
        
        app = App(window, cap)

        while True:
            app.show()
            window.mainloop()
        
    
        


class App():
    def __init__(self, window, vs):
        self.window = window
        self.vs = vs
        self.frame = None
        self.thread = None
        self.stopEvent = None
        self.panel = None
        
        self.stopEvent = threading.Event()
        self.thread = threading.Thread(target=self.videoLoop, args=())
        self.thread.start()


    def show(self):
        title = tk.Label(self.window, text="ARCVision",
                         anchor="center",
                         font=("Times New Roman", 20))
        title.place(relx=0.35, rely=0.1)



    def videoLoop(self):

        try:
            while not self.stopEvent.is_set():
                print("HERE")
                ret, self.frame = self.vs.read()
                self.frame = cv2.resize(self.frame, (300,300))

                # swap the channels becuase openCV uses BGR whereas PIL
                # uses RGB
                image = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
                image = Image.fromarray(image)
                image = ImageTk.PhotoImage(image)

                if self.panel is None:
                    self.panel = tk.Label(image=image)
                    self.panel.image = image
                    self.panel.pack(side="left", padx=10, pady=10)

                else:
                    self.panel.configure(image=image)
                    self.panel.image = image

        except RuntimeError:
            print("[INFO] caught a RuntimeError")
        


if (__name__ == "__main__"):
    window = tk.Tk()
    window.title("ARCVision")
    window.geometry("500x500")
    
    menu = Menu(window)
    menu.show()
    
    window.mainloop()


