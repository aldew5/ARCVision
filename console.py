import tkinter as tk
from tkinter import scrolledtext


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
        # https://www.geeksforgeeks.org/python-tkinter-scrolledtext-widget/
        self.textfield.place(relx=self.x, rely=self.y)
        self.textfield.insert(tk.INSERT, self.cursor)

    def update(self, text):
        self.textfield.insert(tk.INSERT,  "\n" + text)

    def get_text(self):
        a = self.textfield.get('1.0', 'end-1c')
        print(a)
