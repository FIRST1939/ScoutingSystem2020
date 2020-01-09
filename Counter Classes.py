# -*- coding: utf-8 -*-
"""
Created on Thu Jan  9 12:42:19 2020

@author: Mason
"""

from tkinter import *
from tkinter import ttk

class CounterClass:
    point = 0
#    root = Tk()

    def __init__(self, app, x, y, item, textX, textY):
        self.item = item
        self.app = app
        self.x = x
        self.y = y
        self.textX = textX
        self.textY = textY
        
        self.textLbl = Label(self.app, text = item).grid(column=textX, row=textY)
       

        self.DisplayLabel = Label(self.app, text = self.point)
        self.DisplayLabel.grid(column = self.x, row = self.y)
        

        self.Plus1Button = Button(self.app, text = "+", command=self.plus1, bg="green4")
        self.Plus1Button.grid(column = (self.x+1), row = y)

        self.Neg1Button = Button(self.app, text = "-", command=self.neg1, bg="red4")
        self.Neg1Button.grid(column = (self.x-1), row = y)

#        self.root.mainloop()
    
        
   
    def plus1(self):
        self.point += 1
        self.DisplayLabel["text"]=str(self.point)

        
    def neg1(self):
        if self.point  > 0:
            self.point -= 1
            self.DisplayLabel["text"]=str(self.point)
    

 
window = Tk()
 
window.geometry('800x480')
window.title("Counter Class Test")
 
tab_control = ttk.Notebook(window)
 
tab1 = ttk.Frame(tab_control)
 
tab2 = ttk.Frame(tab_control)
 
tab_control.add(tab1, text='First')
 
tab_control.add(tab2, text='Second')
tab_control.pack(expand=1, fill='both') 

lbl1 = Label(tab1, text= 'label1')
 
lbl1.grid(column=0, row=1)
 
lbl2 = Label(tab2, text= 'label2')
 
lbl2.grid(column=0, row=1)
 
count1 = CounterClass(tab1, 2, 0, 'yeet', 0, 0)
count2 = CounterClass(tab2, 2, 0, 'oof', 0, 0)

window.mainloop()