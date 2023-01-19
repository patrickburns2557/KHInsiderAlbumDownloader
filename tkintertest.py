from tkinter import *
from tkinter import ttk

def yes():
    print("yes")



root = Tk()
userInput = StringVar()
frame = ttk.Frame(root, padding=10)
frame.grid()
ttk.Label(frame, text="example text").grid(column=0, row=0)
ttk.Button(frame, text="quit", command=root.destroy).grid(column=1, row=0)
ttk.Button(frame, text="click", command=lambda: print("no")).grid(column=0, row=1)
ttk.Entry(frame, textvariable=userInput).grid(column=0, row=2)
ttk.Button(frame, text="Print Input", command=lambda: [print(userInput.get()), print("text 2")]).grid(column=0, row=3)
list = Listbox(frame)
root.mainloop()
print("Userinput: ", userInput.get())