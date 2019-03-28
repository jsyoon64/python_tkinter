from tkinter import *

class cip_buttons:
 def __init__(self, master):
   self.frame = Frame(master)
   self.printbutton = Button(self.frame, text="print message", command = self.printmessage)
   self.printbutton.pack(side=LEFT)
   self.quitbutton = Button(self.frame, text = "quit", command = self.frame.quit)
   self.quitbutton.pack(side=LEFT)
   self.frame.pack()
 def printmessage(self):
   print("it works!")


var = Tk()
c = cip_buttons(var)
c1 = cip_buttons(var)

var.mainloop()