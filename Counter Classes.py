



# -*- coding: utf-8 -*-
"""
Created on Thu Jan  9 12:42:19 2020

@author: Mason
"""

#from tkinter import *
from tkinter import ttk
from tkinter import Tk
from tkinter import Button
from tkinter import Label

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


class lowGoalCounterClass:
    shotsMade = 0
    shotsTaken = 0

    def __init__(self, app, x, y, item, textX, textY):
        self.item = item
        self.app = app
        self.x = x
        self.y = y
        self.textX = textX
        self.textY = textY
        
        self.textLbl = Label(self.app, text = item).grid(column=textX, row=textY)
       

        self.madeDisplayLabel = Label(self.app, text = self.shotsMade)
        self.madeDisplayLabel.grid(column = (self.x+5), row = self.y)
        

        self.Plus1Button = Button(self.app, text = "+", command=self.madePlus1, bg="green4")
        self.Plus1Button.grid(column = (self.x+6), row = y)

        self.Neg1Button = Button(self.app, text = "-", command=self.madeNeg1, bg="red4")
        self.Neg1Button.grid(column = (self.x+4), row = y)

        self.Plus5Button = Button(self.app, text = "+", command=self.madePlus5, bg="green4")
        self.Plus5Button.grid(column = (self.x+7), row = y)

        self.Neg5Button = Button(self.app, text = "-", command=self.madeNeg5, bg="red4")
        self.Neg5Button.grid(column = (self.x+3), row = y)

        self.takenDisplayLabel = Label(self.app, text = self.shotsTaken)
        self.takenDisplayLabel.grid(column = self.x, row = self.y)
        

        self.takenPlus1Button = Button(self.app, text = "+", command=self.takenPlus1, bg="green4")
        self.takenPlus1Button.grid(column = (self.x+1), row = y)

        self.takenNeg1Button = Button(self.app, text = "-", command=self.takenNeg1, bg="red4")
        self.takenNeg1Button.grid(column = (self.x-1), row = y)

    
        self.takenPlus5Button = Button(self.app, text = "+", command=self.takenPlus5, bg="green4")
        self.takenPlus5Button.grid(column = (self.x+2), row = y, padx=17, sticky='E')

        self.takenNeg5Button = Button(self.app, text = "-", command=self.takenNeg5, bg="red4")
        self.takenNeg5Button.grid(column = (self.x-2), row = y)

#        self.root.mainloop()
    
        
   
    def madePlus5(self):
        self.shotsMade += 5
        self.shotsTaken += 5
        self.madeDisplayLabel["text"]=str(self.shotsMade)
        self.takenDisplayLabel["text"]=str(self.shotsTaken)
        
    def madeNeg5(self):
        if self.shotsMade  >= 5:
            self.shotsMade -= 5
            self.shotsTaken -=5
            self.madeDisplayLabel["text"]=str(self.shotsMade)
            self.takenDisplayLabel["text"]=str(self.shotsTaken)
        else:
            self.shotsMade = 0
            self.shotsTaken = 0
            self.madeDisplayLabel["text"]=str(self.shotsMade)
            self.takenDisplayLabel["text"]=str(self.shotsTaken)
            
    def takenPlus5(self):
#        self.shotsMade += 5
        self.shotsTaken += 5
#        self.madeDisplayLabel["text"]=str(self.shotsMade)
        self.takenDisplayLabel["text"]=str(self.shotsTaken)
        
    def takenNeg5(self):
        if self.shotsTaken  >= self.shotsMade+5:
#            self.shotsMade -= 5
            self.shotsTaken -=5
#            self.madeDisplayLabel["text"]=str(self.shotsMade)
            self.takenDisplayLabel["text"]=str(self.shotsTaken)
        else:
           self.shotsTaken = self.shotsMade
           self.takenDisplayLabel["text"]=str(self.shotsTaken)
    
    def madePlus1(self):
        self.shotsMade += 1
        self.shotsTaken += 1
        self.madeDisplayLabel["text"]=str(self.shotsMade)
        self.takenDisplayLabel["text"]=str(self.shotsTaken)
        
    def madeNeg1(self):
        if self.shotsMade  > 0:
            self.shotsMade -= 1
            self.shotsTaken -=1
            self.madeDisplayLabel["text"]=str(self.shotsMade)
            self.takenDisplayLabel["text"]=str(self.shotsTaken)
            
    def takenPlus1(self):
#        self.shotsMade += 1
        self.shotsTaken += 1
#        self.madeDisplayLabel["text"]=str(self.shotsMade)
        self.takenDisplayLabel["text"]=str(self.shotsTaken)
        
    def takenNeg1(self):
        if self.shotsTaken  > self.shotsMade:
#            self.shotsMade -= 1
            self.shotsTaken -=1
#            self.madeDisplayLabel["text"]=str(self.shotsMade)
            self.takenDisplayLabel["text"]=str(self.shotsTaken)


class highGoalCounterClass:
    innerShotsMade = 0
    outerShotsMade = 0
    shotsTaken = 0

    def __init__(self, app, x, y, item, textX, textY):
        self.item = item
        self.app = app
        self.x = x
        self.y = y
        self.textX = textX
        self.textY = textY
        
        self.textLbl = Label(self.app, text = item).grid(column=textX, row=textY)
       
#inner made
        self.innerMadeDisplayLabel = Label(self.app, text = self.innerShotsMade)
        self.innerMadeDisplayLabel.grid(column = (self.x+5), row = self.y)

        self.innerPlus1Button = Button(self.app, text = "+", command=self.innerMadePlus1, bg="green4")
        self.innerPlus1Button.grid(column = (self.x+6), row = y)

        self.innerNeg1Button = Button(self.app, text = "-", command=self.innerMadeNeg1, bg="red4")
        self.innerNeg1Button.grid(column = (self.x+4), row = y)

        self.innerPlus5Button = Button(self.app, text = "+", command=self.innerMadePlus5, bg="green4")
        self.innerPlus5Button.grid(column = (self.x+7), row = y)

        self.innerNeg5Button = Button(self.app, text = "-", command=self.innerMadeNeg5, bg="red4")
        self.innerNeg5Button.grid(column = (self.x+3), row = y)

#outer made
        self.outerMadeDisplayLabel = Label(self.app, text = self.outerShotsMade)
        self.outerMadeDisplayLabel.grid(column = (self.x+5), row = self.y+1)        

        self.outerPlus1Button = Button(self.app, text = "+", command=self.outerMadePlus1, bg="green4")
        self.outerPlus1Button.grid(column = (self.x+6), row = y+1)

        self.outerNeg1Button = Button(self.app, text = "-", command=self.outerMadeNeg1, bg="red4")
        self.outerNeg1Button.grid(column = (self.x+4), row = y+1)

        self.outerPlus5Button = Button(self.app, text = "+", command=self.outerMadePlus5, bg="green4")
        self.outerPlus5Button.grid(column = (self.x+7), row = y+1)

        self.outerNeg5Button = Button(self.app, text = "-", command=self.outerMadeNeg5, bg="red4")
        self.outerNeg5Button.grid(column = (self.x+3), row = y+1)

#taken
        self.takenDisplayLabel = Label(self.app, text = self.shotsTaken)
        self.takenDisplayLabel.grid(column = self.x, row = self.y)
        
        self.takenPlus1Button = Button(self.app, text = "+", command=self.takenPlus1, bg="green4")
        self.takenPlus1Button.grid(column = (self.x+1), row = y)

        self.takenNeg1Button = Button(self.app, text = "-", command=self.takenNeg1, bg="red4")
        self.takenNeg1Button.grid(column = (self.x-1), row = y)

    
        self.takenPlus5Button = Button(self.app, text = "+", command=self.takenPlus5, bg="green4")
        self.takenPlus5Button.grid(column = (self.x+2), row = y, padx=17, sticky='E')

        self.takenNeg5Button = Button(self.app, text = "-", command=self.takenNeg5, bg="red4")
        self.takenNeg5Button.grid(column = (self.x-2), row = y)

#        self.root.mainloop()
    
        
#inner made def   
    def innerMadePlus5(self):
        self.innerShotsMade += 5
        self.shotsTaken += 5
        self.innerMadeDisplayLabel["text"]=str(self.innerShotsMade)
        self.takenDisplayLabel["text"]=str(self.shotsTaken)
        
    def innerMadeNeg5(self):
        if self.innerShotsMade  >= 5:
            self.innerShotsMade -= 5
            self.shotsTaken -=5
            self.innerMadeDisplayLabel["text"]=str(self.innerShotsMade)
            self.takenDisplayLabel["text"]=str(self.shotsTaken)
        else:
            self.innerShotsMade = 0
            self.shotsTaken = 0
            self.madeDisplayLabel["text"]=str(self.innerShotsMade)
            self.takenDisplayLabel["text"]=str(self.shotsTaken)
            

    def innerMadePlus1(self):
        self.innerShotsMade += 1
        self.shotsTaken += 1
        self.innerMadeDisplayLabel["text"]=str(self.innerShotsMade)
        self.takenDisplayLabel["text"]=str(self.shotsTaken)
        
    def innerMadeNeg1(self):
        if self.innerShotsMade  > 0:
            self.innerShotsMade -= 1
            self.shotsTaken -=1
            self.innerMadeDisplayLabel["text"]=str(self.innerShotsMade)
            self.takenDisplayLabel["text"]=str(self.shotsTaken)

#outer made def
    def outerMadePlus5(self):
        self.outerShotsMade += 5
        self.shotsTaken += 5
        self.outerMadeDisplayLabel["text"]=str(self.outerShotsMade)
        self.takenDisplayLabel["text"]=str(self.shotsTaken)
        
    def outerMadeNeg5(self):
        if self.outerShotsMade  >= 5:
            self.outerShotsMade -= 5
            self.shotsTaken -=5
            self.outerMadeDisplayLabel["text"]=str(self.outerShotsMade)
            self.takenDisplayLabel["text"]=str(self.shotsTaken)
        else:
            self.outerShotsMade = 0
            self.shotsTaken = 0
            self.madeDisplayLabel["text"]=str(self.outerShotsMade)
            self.takenDisplayLabel["text"]=str(self.shotsTaken)
            

    def outerMadePlus1(self):
        self.outerShotsMade += 1
        self.shotsTaken += 1
        self.outerMadeDisplayLabel["text"]=str(self.outerShotsMade)
        self.takenDisplayLabel["text"]=str(self.shotsTaken)
        
    def outerMadeNeg1(self):
        if self.outerShotsMade  > 0:
            self.outerShotsMade -= 1
            self.shotsTaken -=1
            self.outerMadeDisplayLabel["text"]=str(self.outerShotsMade)
            self.takenDisplayLabel["text"]=str(self.shotsTaken)


#taken def
    def takenPlus5(self):
#        self.shotsMade += 5
        self.shotsTaken += 5
#        self.madeDisplayLabel["text"]=str(self.shotsMade)
        self.takenDisplayLabel["text"]=str(self.shotsTaken)
        
    def takenNeg5(self):
        if self.shotsTaken  >= self.outerShotsMade + self.innerShotsMade +5:
#            self.shotsMade -= 5
            self.shotsTaken -=5
#            self.madeDisplayLabel["text"]=str(self.shotsMade)
            self.takenDisplayLabel["text"]=str(self.shotsTaken)
        else:
           self.shotsTaken = self.innerShotsMade + self.outerShotsMade
           self.takenDisplayLabel["text"]=str(self.shotsTaken)
                
    def takenPlus1(self):
#        self.shotsMade += 1
        self.shotsTaken += 1
#        self.madeDisplayLabel["text"]=str(self.shotsMade)
        self.takenDisplayLabel["text"]=str(self.shotsTaken)
        
    def takenNeg1(self):
        if self.shotsTaken  > self.innerShotsMade + self.outerShotsMade:
#            self.shotsMade -= 1
            self.shotsTaken -=1
#            self.madeDisplayLabel["text"]=str(self.shotsMade)
            self.takenDisplayLabel["text"]=str(self.shotsTaken)
            
def clicked():
    print(count1.point)
    print(count2.point)
    print(bigBoi.shotsTaken)
    print(bigBoi.shotsMade)
    print(highAsAKite.shotsMade)
    print(highAsAKite.innerShotsMade)
    print(highAsAKite.outerShotsMade)
    
    
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
bigBoi = lowGoalCounterClass(tab2, 3, 2, 'whatever', 0, 2)
highAsAKite = highGoalCounterClass(tab2, 3, 3, 'done', 0, 3)

printBtn = Button(tab1, text = 'print this thing', command = clicked)
printBtn.grid(column = 1, row=1)
window.mainloop()

Reply
Forward

