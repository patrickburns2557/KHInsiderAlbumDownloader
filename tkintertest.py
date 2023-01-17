from tkinter import *
from tkinter import ttk

def yes():
    print("yes")

root = Tk()
frame = ttk.Frame(root, padding=10)
frame.grid()
ttk.Label(frame, text="example text").grid(column=0, row=0)
ttk.Button(frame, text="quit", command=root.destroy).grid(column=1, row=0)
ttk.Button(frame, text="click", command=lambda: print("no")).grid(column=0, row=1)
root.mainloop()