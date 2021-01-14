import tkinter as tk



class Menu(tk.Frame):
    def __init__(self, window):
        self.window = window

    def show(self):
        title = tk.Label(self.window, text="ARCVision",
                         anchor="center",
                         font=("Times New Roman", 20))
        title.place(relx=0.35, rely=0.3)

        checked = tk.IntVar()
        box = tk.Checkbutton(window, text="Enable descriptors", variable=checked)
        box.place(relx=0.35, rely=0.4)

        start = tk.Button(window,
                          text="Start Application",
                          command=self.destroy,
                          bg="green")
        start.place(relx=0.35, rely=0.5)

    def destroy(self):
        self.window.destroy()
        window = tk.Tk()
        window.title("ARCVision")
        window.geometry("500x500")
        
        app = App(window)
        app.show()
    
        


class App():
    def __init__(self, window):
        self.window = window

    def show(self):
        title = tk.Label(self.window, text="ARCVision",
                         anchor="center",
                         font=("Times New Roman", 20))
        title.place(relx=0.35, rely=0.1)


if (__name__ == "__main__"):
    window = tk.Tk()
    window.title("ARCVision")
    window.geometry("500x500")
    
    menu = Menu(window)
    menu.show()

    window.mainloop()


