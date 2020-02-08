#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 16 17:41:34 2020

@author: caroline
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 16 16:34:18 2020

@author: caroline
"""

#imports
from tkinter import Tk
from tkinter import Button
from tkinter import Label
from tkinter import Checkbutton
from tkinter import Canvas
from tkinter import BOTH
from tkinter import RIGHT
from tkinter import Text
from tkinter import Radiobutton
from tkinter import BooleanVar
from tkinter import IntVar
from tkinter import ttk
from tkinter import font
from tkinter import messagebox
from tkinter import END
#import match_dbconn
import sys
#import psutil
#from time import sleep
from PIL import ImageTk, Image

#global vars
global autoCycles
global teleCycles
global lowGoalMisses
global highGoalMisses
global lowGoalMakes
global innerGoalMakes
global outerGoalMakes
autoCycles = 0
teleCycles = 0
lowGoalMisses = [0,0]
highGoalMisses = [0,0]
lowGoalMakes = [0,0]
innerGoalMakes = [0,0]
outerGoalMakes = [0,0]


class CounterClass:
    point = 0
#    root = Tk()

    def __init__(self, app, x, y, item, textX, textY, textXSpan):
        self.item = item
        self.app = app
        self.x = x
        self.y = y
        self.textX = textX
        self.textY = textY
        self.textXSpan = textXSpan
        
        self.textLbl = Label(self.app, text = item).grid(column=textX, row=textY, columnspan=self.textXSpan)
       

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
    
    def reinit(self):
        self.DisplayLabel["text"]=str(self.point)


class lowGoalCounterClass:
    shotsMade = 0
    shotsMissed = 0

    def __init__(self, app, x, y, item, textX, textY):
        self.item = item
        self.app = app
        self.x = x
        self.y = y
        self.textX = textX
        self.textY = textY
        
        self.textLbl = Label(self.app, text = item).grid(column=textX, row=textY)
        self.spaceLBL = Label(self.app, text='                        Low  ').grid(column=x+3, row=y)

        self.madeDisplayLabel = Label(self.app, text = self.shotsMade)
        self.madeDisplayLabel.grid(column = (self.x+6), row = self.y)
        

        self.Plus1Button = Button(self.app, text = "+1", command=self.madePlus1, bg="green4")
        self.Plus1Button.grid(column = (self.x+7), row = y)

        self.Neg1Button = Button(self.app, text = "-1", command=self.madeNeg1, bg="red4")
        self.Neg1Button.grid(column = (self.x+5), row = y)

        self.Plus5Button = Button(self.app, text = "+5", command=self.madePlus5, bg="green4")
        self.Plus5Button.grid(column = (self.x+8), row = y)

        self.Neg5Button = Button(self.app, text = "-5", command=self.madeNeg5, bg="red4")
        self.Neg5Button.grid(column = (self.x+4), row = y)

        self.takenDisplayLabel = Label(self.app, text = self.shotsMissed)
        self.takenDisplayLabel.grid(column = self.x, row = self.y)
        

        self.takenPlus1Button = Button(self.app, text = "+1", command=self.takenPlus1, bg="green4")
        self.takenPlus1Button.grid(column = (self.x+1), row = y)

        self.takenNeg1Button = Button(self.app, text = "-1", command=self.takenNeg1, bg="red4")
        self.takenNeg1Button.grid(column = (self.x-1), row = y)

    
        self.takenPlus5Button = Button(self.app, text = "+5", command=self.takenPlus5, bg="green4")
        self.takenPlus5Button.grid(column = (self.x+2), row = y, sticky='W')

        self.takenNeg5Button = Button(self.app, text = "-5", command=self.takenNeg5, bg="red4")
        self.takenNeg5Button.grid(column = (self.x-2), row = y)

#        self.root.mainloop()
    
        
   
    def madePlus5(self):
        self.shotsMade += 5
#        self.shotsMissed += 5
        self.madeDisplayLabel["text"]=str(self.shotsMade)
#        self.takenDisplayLabel["text"]=str(self.shotsMissed)
        
    def madeNeg5(self):
        if self.shotsMade  >= 5:
            self.shotsMade -= 5
#            self.shotsMissed -=5
            self.madeDisplayLabel["text"]=str(self.shotsMade)
#            self.takenDisplayLabel["text"]=str(self.shotsMissed)
        else:
            self.shotsMade = 0
            self.shotsMissed = 0
            self.madeDisplayLabel["text"]=str(self.shotsMade)
            self.takenDisplayLabel["text"]=str(self.shotsMissed)
            
    def takenPlus5(self):
#        self.shotsMade += 5
        self.shotsMissed += 5
#        self.madeDisplayLabel["text"]=str(self.shotsMade)
        self.takenDisplayLabel["text"]=str(self.shotsMissed)
        
    def takenNeg5(self):
        if self.shotsMissed  >5:
#            self.shotsMade -= 5
            self.shotsMissed -=5
#            self.madeDisplayLabel["text"]=str(self.shotsMade)
            self.takenDisplayLabel["text"]=str(self.shotsMissed)
        else:
           self.shotsMissed = 0
           self.takenDisplayLabel["text"]=str(self.shotsMissed)
    
    def madePlus1(self):
        self.shotsMade += 1
#        self.shotsMissed += 1
        self.madeDisplayLabel["text"]=str(self.shotsMade)
        self.takenDisplayLabel["text"]=str(self.shotsMissed)
        
    def madeNeg1(self):
        if self.shotsMade  > 0:
            self.shotsMade -= 1
#            self.shotsMissed -=1
            self.madeDisplayLabel["text"]=str(self.shotsMade)
            self.takenDisplayLabel["text"]=str(self.shotsMissed)
            
    def takenPlus1(self):
#        self.shotsMade += 1
        self.shotsMissed += 1
#        self.madeDisplayLabel["text"]=str(self.shotsMade)
        self.takenDisplayLabel["text"]=str(self.shotsMissed)
        
    def takenNeg1(self):
        if self.shotsMissed  > 0:
#            self.shotsMade -= 1
            self.shotsMissed -=1
#            self.madeDisplayLabel["text"]=str(self.shotsMade)
            self.takenDisplayLabel["text"]=str(self.shotsMissed)
            
    def reinit(self):
         self.takenDisplayLabel["text"]=str(self.shotsMissed)
         self.madeDisplayLabel["text"]=str(self.shotsMade)
         


class highGoalCounterClass:
    innerShotsMade = 0
    outerShotsMade = 0
    shotsMissed = 0

    def __init__(self, app, x, y, item, textX, textY):
        self.item = item
        self.app = app
        self.x = x
        self.y = y
        self.textX = textX
        self.textY = textY
        
        self.textLbl = Label(self.app, text = item).grid(column=textX, row=textY)
        self.spaceLBL = Label(self.app, text='                        Outer ').grid(column=x+3, row=y+1)
        self.spaceLBL2 = Label(self.app, text='                        Inner ').grid(column=x+3, row=y)
       
#inner made
        self.innerMadeDisplayLabel = Label(self.app, text = self.innerShotsMade)
        self.innerMadeDisplayLabel.grid(column = (self.x+6), row = self.y)

        self.innerPlus1Button = Button(self.app, text = "+1", command=self.innerMadePlus1, bg="green4")
        self.innerPlus1Button.grid(column = (self.x+7), row = y)

        self.innerNeg1Button = Button(self.app, text = "-1", command=self.innerMadeNeg1, bg="red4")
        self.innerNeg1Button.grid(column = (self.x+5), row = y)

        self.innerPlus5Button = Button(self.app, text = "+5", command=self.innerMadePlus5, bg="green4")
        self.innerPlus5Button.grid(column = (self.x+8), row = y)

        self.innerNeg5Button = Button(self.app, text = "-5", command=self.innerMadeNeg5, bg="red4")
        self.innerNeg5Button.grid(column = (self.x+4), row = y)

#outer made
        self.outerMadeDisplayLabel = Label(self.app, text = self.outerShotsMade)
        self.outerMadeDisplayLabel.grid(column = (self.x+6), row = self.y+1)        

        self.outerPlus1Button = Button(self.app, text = "+1", command=self.outerMadePlus1, bg="green4")
        self.outerPlus1Button.grid(column = (self.x+7), row = y+1)

        self.outerNeg1Button = Button(self.app, text = "-1", command=self.outerMadeNeg1, bg="red4")
        self.outerNeg1Button.grid(column = (self.x+5), row = y+1)

        self.outerPlus5Button = Button(self.app, text = "+5", command=self.outerMadePlus5, bg="green4")
        self.outerPlus5Button.grid(column = (self.x+8), row = y+1)

        self.outerNeg5Button = Button(self.app, text = "-5", command=self.outerMadeNeg5, bg="red4")
        self.outerNeg5Button.grid(column = (self.x+4), row = y+1)

#taken
        self.takenDisplayLabel = Label(self.app, text = self.shotsMissed)
        self.takenDisplayLabel.grid(column = self.x, row = self.y)
        
        self.takenPlus1Button = Button(self.app, text = "+1", command=self.takenPlus1, bg="green4")
        self.takenPlus1Button.grid(column = (self.x+1), row = y)

        self.takenNeg1Button = Button(self.app, text = "-1", command=self.takenNeg1, bg="red4")
        self.takenNeg1Button.grid(column = (self.x-1), row = y)

    
        self.takenPlus5Button = Button(self.app, text = "+5", command=self.takenPlus5, bg="green4")
        self.takenPlus5Button.grid(column = (self.x+2), row = y, sticky='W')

        self.takenNeg5Button = Button(self.app, text = "-5", command=self.takenNeg5, bg="red4")
        self.takenNeg5Button.grid(column = (self.x-2), row = y)

#        self.root.mainloop()
    
        
#inner made def   
    def innerMadePlus5(self):
        self.innerShotsMade += 5
#        self.shotsMissed += 5
        self.innerMadeDisplayLabel["text"]=str(self.innerShotsMade)
        self.takenDisplayLabel["text"]=str(self.shotsMissed)
        
    def innerMadeNeg5(self):
        if self.innerShotsMade  >= 5:
            self.innerShotsMade -= 5
#            self.shotsMissed -=5
            self.innerMadeDisplayLabel["text"]=str(self.innerShotsMade)
            self.takenDisplayLabel["text"]=str(self.shotsMissed)
        else:
            self.innerShotsMade = 0
#            self.shotsMissed = 0
            self.madeDisplayLabel["text"]=str(self.innerShotsMade)
            self.takenDisplayLabel["text"]=str(self.shotsMissed)
            

    def innerMadePlus1(self):
        self.innerShotsMade += 1
#        self.shotsMissed += 1
        self.innerMadeDisplayLabel["text"]=str(self.innerShotsMade)
        self.takenDisplayLabel["text"]=str(self.shotsMissed)
        
    def innerMadeNeg1(self):
        if self.innerShotsMade  > 0:
            self.innerShotsMade -= 1
#            self.shotsMissed -=1
            self.innerMadeDisplayLabel["text"]=str(self.innerShotsMade)
            self.takenDisplayLabel["text"]=str(self.shotsMissed)

#outer made def
    def outerMadePlus5(self):
        self.outerShotsMade += 5
#        self.shotsMissed += 5
        self.outerMadeDisplayLabel["text"]=str(self.outerShotsMade)
        self.takenDisplayLabel["text"]=str(self.shotsMissed)
        
    def outerMadeNeg5(self):
        if self.outerShotsMade  >= 5:
            self.outerShotsMade -= 5
#            self.shotsMissed -=5
            self.outerMadeDisplayLabel["text"]=str(self.outerShotsMade)
            self.takenDisplayLabel["text"]=str(self.shotsMissed)
        else:
            self.outerShotsMade = 0
#            self.shotsMissed = 0
            self.madeDisplayLabel["text"]=str(self.outerShotsMade)
            self.takenDisplayLabel["text"]=str(self.shotsMissed)
            

    def outerMadePlus1(self):
        self.outerShotsMade += 1
#        self.shotsMissed += 1
        self.outerMadeDisplayLabel["text"]=str(self.outerShotsMade)
        self.takenDisplayLabel["text"]=str(self.shotsMissed)
        
    def outerMadeNeg1(self):
        if self.outerShotsMade  > 0:
            self.outerShotsMade -= 1
#            self.shotsMissed -=1
            self.outerMadeDisplayLabel["text"]=str(self.outerShotsMade)
            self.takenDisplayLabel["text"]=str(self.shotsMissed)


#taken def
    def takenPlus5(self):
#        self.shotsMade += 5
        self.shotsMissed += 5
#        self.madeDisplayLabel["text"]=str(self.shotsMade)
        self.takenDisplayLabel["text"]=str(self.shotsMissed)
        
    def takenNeg5(self):
        if self.shotsMissed  >5:
#            self.shotsMade -= 5
            self.shotsMissed -=5
#            self.madeDisplayLabel["text"]=str(self.shotsMade)
            self.takenDisplayLabel["text"]=str(self.shotsMissed)
        else:
           self.shotsMissed = 0
           self.takenDisplayLabel["text"]=str(self.shotsMissed)
                
    def takenPlus1(self):
#        self.shotsMade += 1
        self.shotsMissed += 1
#        self.madeDisplayLabel["text"]=str(self.shotsMade)
        self.takenDisplayLabel["text"]=str(self.shotsMissed)
        
    def takenNeg1(self):
        if self.shotsMissed  > 0:
#            self.shotsMade -= 1
            self.shotsMissed -=1
#            self.madeDisplayLabel["text"]=str(self.shotsMade)
            self.takenDisplayLabel["text"]=str(self.shotsMissed)

    def reinit(self):
         self.takenDisplayLabel["text"]=str(self.shotsMissed)
         self.outerMadeDisplayLabel["text"]=str(self.outerShotsMade)
         self.innerMadeDisplayLabel["text"]=str(self.innerShotsMade)

#some data base stuff
#def getTeam():
#    team_no = match_dbconn.getMatchInfo(match_no,position)
#    title_str = "MATCH NO: %s TEAM NO: %s  Postion %s" %(match_no,team_no,position)
#    window.title(title_str)
#    print(team_no)
#    global teamno
#    teamno = team_no
#    
#def getNextMatch():
#   new_match_no = match_dbconn.getNextMatch();
#   print('new match %s',new_match_no)
#   global match_no
#   global position
#   print('current match %s',match_no)
#   if new_match_no != match_no:
#       print('reinitialize screens')
#       match_no = new_match_no
#       getTeam()
#       match_dbconn.setScout(scoutName.get(),match_no,position)
#   window.after(2000,getNextMatch)
#
def cycleReinit(gamePhase):
    print('cycle reinit ran')
    global autoCycles
    global teleCycles
    if gamePhase == 0:
        autoLow.shotsMissed = 0
        autoHigh.shotsMissed = 0
        autoLow.shotsMade = 0
        autoHigh.innerShotsMade = 0
        autoHigh.outerShotsMade = 0
        autoCycles += 1
        autoLow.reinit()
        autoHigh.reinit()  
        print('auto reinitialized')
        
    else:
        teleLowGoal.shotsMissed = 0
        teleHighGoal.shotsMissed = 0
        teleLowGoal.shotsMade = 0
        teleHighGoal.innerShotsMade = 0
        teleHighGoal.outerShotsMade = 0
        teleCycles += 1
        teleLowGoal.reinit()
        teleHighGoal.reinit()
        print('tele reinitialized')
#
#def sendMainToDatabase(cards):
#    global lowGoalMisses
#    global highGoalMisses
#    global lowGoalMakes
#    global innerGoalMakes
#    global outerGoalMakes
#    match_dbconn.setMatchScout(match_no, 
#                               teamno,
#                               scoutName.get(),
#                               teamnum.get(),
#                               autoStartPos.get(),
#                               crossLine_State.get(),
#                               autoShooterPos.get(),
#                               lowGoalMisses[0],
#                               highGoalMisses[0],
#                               lowGoalMakes[0],
#                               outerGoalMakes[0],
#                               innerGoalMakes[0],
#                               autoBallsPickedUp.point,
#                               autoFoul.point,
#                               autoTechFoul.point,
#                               shooterPos.get(),
#                               lowGoalMisses[1],
#                               highGoalMisses[1],
#                               lowGoalMakes[1],
#                               outerGoalMakes[1],
#                               innerGoalMakes[1],
#                               teleFoul.point,
#                               teleTechFoul.point,
#                               defense_State.get(),
#                               rotationalControl.get(),
#                               positionalControl.get(),
#                               fellOffBar_State.get(),
#                               buddyClimb_State.get(),
#                               hitOpponent_State.get(),
#                               leveledBar_State.get(),
#                               climbFrom.get(),
#                               barLevel.get(),
#                               deadbot_State.get(),
#                               comments.get("1.0", END),
#                               tippedOver_State.get(),
#                               recoveredFromDead_State.get(),
#                               cards
#                               )

#def popup_keyboard(event):
##    os.popen('matchbox-keyboard','r',4096)
#    PROCNAME = "florence"
#    for ploc in psutil.process_iter():
#        if proc.name() == PROCNAME:
#            proc.kill()
#    sleep(0.5)
#    os.popen('/usr/bin/florence')
    
#def sendCycleToDatabase(gamePhase):
#    print('send to database function ran')
#    global autoCycles
#    global teleCycles
#    global lowGoalMisses
#    global highGoalMisses
#    global lowGoalMakes
#    global innerGoalMakes
#    global outerGoalMakes
#    if gamePhase == 0: 
#        lowGoalMisses[0] += autoLow.shotsMissed
#        highGoalMisses[0] += autoHigh.shotsMissed
#        lowGoalMakes[0] += autoLow.shotsMade
#        outerGoalMakes[0] += autoHigh.outerShotsMade
#        innerGoalMakes[0] += autoHigh.innerShotsMade
#        
#        match_dbconn.setMatchCycle(autoCycles,
#                                   match_no, 
#                                   teamno, 
#                                   autoShooterPos.get(),
#                                   autoLow.shotsMissed,
#                                   autoHigh.shotsMissed,
#                                   autoLow.shotsMade,
#                                   autoHigh.outerShotsMade,
#                                   autoHigh.innerShotsMade,
#                                   gamePhase)
#        print('Sent auto to database')
#        autoCycles = (autoCycles+1)
#        print('increment autoCycles complete')
#    else: 
#        lowGoalMisses[1] += teleLowGoal.shotsMissed
#        highGoalMisses[1] += teleHighGoal.shotsMissed
#        lowGoalMakes[1] += teleLowGoal.shotsMade
#        outerGoalMakes[1] += teleHighGoal.outerShotsMade
#        innerGoalMakes[1] += teleHighGoal.innerShotsMade
#        match_dbconn.setMatchCycle(teleCycles,
#                                   match_no, 
#                                   teamno, 
#                                   shooterPos.get(),
#                                   teleLowGoal.shotsMissed,
#                                   teleHighGoal.shotsMissed,
#                                   teleLowGoal.shotsMade,
#                                   teleHighGoal.outerShotsMade,
#                                   teleHighGoal.innerShotsMade,
#                                   gamePhase)
#        print('sent tele cycles to database')
#        teleCycles = (teleCycles+1)
#       
def sendCycleData(gamePhase):
    if  (gamePhase == 1 and teleLowGoal.shotsMissed == 0 and teleHighGoal.shotsMissed == 0 and teleLowGoal.shotsMade == 0 and teleHighGoal.outerShotsMade == 0 and teleHighGoal.innerShotsMade == 0):
        messagebox.showinfo('No data', 'You haven\'t recorded any shots for this cycle yet')
    elif (gamePhase == 0 and autoLow.shotsMissed == 0 and autoHigh.shotsMissed == 0 and autoLow.shotsMade == 0 and autoHigh.outerShotsMade == 0 and autoHigh.innerShotsMade ==0):
        messagebox.showinfo('No data', 'You haven\'t recorded any shots for this cycle yet')
        
    else:
        #send data
#        sendCycleToDatabase(gamePhase)
        cycleReinit(gamePhase)
    print('done!')

    #reinitialize cycle 
#    sendCycleToDatabase(gamePhase)
#
def getCardValue():
    cardValue=0
    if yellowCard_State.get() !=0:
        cardValue=1
    if redCard_State.get() !=0:
        cardValue=2
    return cardValue
#                         
#def sendMainData():
#    global autoCycles
#    global teleCycles
#    sendMSG = messagebox.askokcancel('Are you sure?', 'If you are ready to send click ok. If you are not ready click cancel, and click send again when you are ready.')
#    if sendMSG is True and dontUseThisData_State.get() is False:
#        if  (teleLowGoal.shotsMissed != 0 or teleHighGoal.shotsMissed != 0 or teleLowGoal.shotsMade != 0 or teleHighGoal.outerShotsMade != 0 or teleHighGoal.innerShotsMade != 0):
#            sendCycleData(1)
#        if (autoLow.shotsMissed != 0 or autoHigh.shotsMissed != 0 or autoLow.shotsMade != 0 or autoHigh.outerShotsMade != 0 or autoHigh.innerShotsMade !=0):
#            sendCycleData(0)
#        autoCycles = 0
#        teleCycles = 0
#        sendMainToDatabase(getCardValue())
#        reinitscreen()
#    elif sendMSG is True and dontUseThisData_State.get() is True:
#        autoCycles = 0
#        teleCycles = 0
#        reinitscreen()
#        
#def screenClear():
#    pass
#
def reinitscreen():
    #auto tab
    crossLine_State.set(False)
    telePrep_State.set(False)
    autoFoul.point = 0
    autoFoul.reinit()
    autoTechFoul.point = 0
    autoTechFoul.reinit()
    autoBallsPickedUp.point =0
    autoBallsPickedUp.reinit()
    #tele page
    teleFoul.point = 0
    teleFoul.reinit()
    teleTechFoul.point = 0
    teleTechFoul.reinit()
    defense_State.set(False)
    rotationalControl.set('No attempt')
    positionalControl.set('No attempt')
    #End game
    fellOffBar_State.set(False)
    buddyClimb_State.set(False)
    hitOpponent_State.set(False)
    leveledBar_State.set(False)
    barLevel.set("No Climb")
    #post match
    deadbot_State.set(False)
    recoveredFromDead_State.set(False)
    tippedOver_State.set(False)
    yellowCard_State.set(False)
    redCard_State.set(False)
    comments.delete(1.0, END)
    dontUseThisData_State.set(False)

def refImagePositionSet(event):
    position = shooterPosRef.get()
    shooterPos.set(position)
    autoShooterPos.set(position)

def autoPositionSet(event):
    position = autoShooterPos.get()
    shooterPosRef.set(position)
    shooterPos.set(position)

def telePositionSet(event):
    position = shooterPos.get()
    shooterPosRef.set(position)
    autoShooterPos.set(position)

#print(teamno)
#opening tkinter
window = Tk() 
window.geometry('800x480')

#window.title('scouting app 2020')

#Give it some style
style = ttk.Style()
style.theme_settings("default",{"TNotebook.Tab":{"configure":{"padding":[20,20]}}})
labelfont = font.Font(family= "times", size= 20)
window.option_add("*Font", labelfont)
labelfont = ('times', 15)
labelfont2 = ('times', 5)

    #edit the tabs here as needed
tab_control = ttk.Notebook(window)
preMatch = ttk.Frame(tab_control)
auto = ttk.Frame(tab_control)
reference = ttk.Frame(tab_control)
tele = ttk.Frame(tab_control)
endGame = ttk.Frame(tab_control)
postMatch = ttk.Frame(tab_control)
tab_control.add(preMatch, text='Pre-Match')
tab_control.add(auto, text='Auto')
tab_control.add(reference, text='Reference Image')
tab_control.add(tele, text='TeleOp')
tab_control.add(endGame, text='End Game')
tab_control.add(postMatch, text='PostMatch')
tab_control.pack(expand=1, fill='both')

#Prematch Screen
scoutName = ttk.Entry(preMatch, width= 30)
#scoutName.bind('<Button-1>', popup_keyboard)
scoutName.grid(column=1, row=0, columnspan=4)
nameLBL = Label(preMatch, text = 'Name:')
nameLBL.grid(column=0, row=0, ipady=17)

teamnum = ttk.Entry(preMatch, width=10)
#teamnum.bind('<Button-1>' , popup_keyboard)
teamnum.grid(column=7, row=0)
teamnumLBL = Label(preMatch, text='  Team# you are with:')
teamnumLBL.grid(row=0, column=5, columnspan=2)

autoStartPos = IntVar()
aLocation = Radiobutton(preMatch, text = 'A', value = 0, var=autoStartPos)
aLocation.grid(row=1, column=0)
bLocation = Radiobutton(preMatch, text='B', value = 1, var=autoStartPos)
bLocation.grid(row=1, column=1)
cLocation = Radiobutton(preMatch, text = 'C', value = 2, var=autoStartPos)
cLocation.grid(row=1, column=2)
dLocation = Radiobutton(preMatch, text = 'D', value = 3, var=autoStartPos)
dLocation.grid(row=1, column=3)
eLocation = Radiobutton(preMatch, text = 'E', value = 4, var=autoStartPos)
eLocation.grid(row=1, column=4)
fLocation = Radiobutton(preMatch, text = 'F', value = 5, var=autoStartPos)
fLocation.grid(row=1, column=5)
gLocation = Radiobutton(preMatch, text = 'G', value = 6, var=autoStartPos)
gLocation.grid(row=1, column=6, ipadx=14)
#hLocation = Radiobutton(preMatch, text = 'H', value = 7, var=autoStartPos)
#hLocation.grid(row=1, column=7, ipadx=17)

startPosImage=Image.open('the map of maps.png')
startPosPhoto=ImageTk.PhotoImage(startPosImage)

startPosLabel=Label(preMatch, image=startPosPhoto)
startPosLabel.image=startPosPhoto
startPosLabel.grid(column=0, row=5, columnspan=5)

#auto screen
autoMissesLBL = Label(auto, text='Misses')
autoMissesLBL.grid(column=1, row=0, columnspan=5)

autoMakesLBL = Label(auto, text='Makes')
autoMakesLBL.grid(column=7, row=0, columnspan=5)

crossLine_State = BooleanVar(False)
crossLine = Checkbutton(auto, text='Crossed Start Line?', var=crossLine_State)
crossLine.grid(row=8, column=7, columnspan=5, ipadx=30)

telePrep_State = BooleanVar(False)
telePrep = Checkbutton(auto, text='Prepared for Teleop?', var=telePrep_State)
telePrep.grid(row=9, column=7, columnspan=5, ipadx=30)

autoFoul = CounterClass(auto, 4, 7, '       Foul', 0, 7, 3)
autoTechFoul = CounterClass(auto, 4, 8, '     Tech Foul', 0, 8, 3)
autoLow = lowGoalCounterClass(auto, 3, 1, '     Low', 0, 1)
autoHigh = highGoalCounterClass(auto, 3, 2, '     High', 0, 2)
autoBallsPickedUp = CounterClass(auto, 4, 6, 'Balls Picked Up', 0, 6, 3)

autoShooterPos = Label(auto, text='Shooter Position')
autoShooterPos.grid(column=0, row=4, columnspan=6, ipady=15, ipadx=10)
autoShooterPos = ttk.Combobox(auto)
autoShooterPos['values']= ("A", "B", "C", "D", "E", "F", "G", "H")
autoShooterPos.current(0)
autoShooterPos.grid(column= 5, row= 4, columnspan= 1, ipady=15, ipadx=10)
autoShooterPos.config(width= 5)
autoShooterPos.bind("<<ComboboxSelected>>", autoPositionSet )


autoEnter = Button(auto, text='enter', command=lambda: sendCycleData(0))
autoEnter.grid(row=4, column=7, rowspan=4, columnspan=6, ipady=15, ipadx=15)

#reference image
image = Image.open('Reference Image.jpg')
canvas = Canvas(reference,width = 600, height = 360)
photo = ImageTk.PhotoImage(image)
canvas.pack(expand=True,fill=BOTH)
canvas.create_image(300,190,image=photo)

shooterPosLBLRef = Label(reference, text='Shooter Position')
shooterPosLBLRef.pack(side=RIGHT)
shooterPosRef = ttk.Combobox(reference)
shooterPosRef['values']= ("A", "B", "C", "D", "E", "F", "G", "H")
shooterPosRef.current(0)
shooterPosRef.pack(side=RIGHT)
shooterPosRef.config(width= 5)
shooterPosRef.bind("<<ComboboxSelected>>", refImagePositionSet )

#TELEOP pagE
            
teleFoul = CounterClass(tele, 3, 10, 'Foul', 0, 10, 1)
teleTechFoul = CounterClass(tele, 9, 10, 'Tech Foul', 6, 10, 1)
teleLowGoal = lowGoalCounterClass(tele, 3, 1, 'Low', 0, 1)
teleHighGoal = highGoalCounterClass(tele, 3, 2, 'Inner', 0, 2)
teleHighGoalLBL = Label(tele, text= 'Outer')
teleHighGoalLBL.grid(column=0, row=3)

rotationalControlLBL = Label(tele, text='Has Rotational Control?')
rotationalControlLBL.grid(column=0, row=9, ipady=23)
rotationalControl = ttk.Combobox(tele)
rotationalControl['values']= ("No attempt","No", "Yes")
rotationalControl.current(0)
rotationalControl.grid(column= 1, row= 9, columnspan=5)
rotationalControl.config(width= 5)
#
positionalControlLBL = Label(tele, text='Has Positional Control?')
positionalControlLBL.grid(column=8, row=9, columnspan=5)
positionalControl = ttk.Combobox(tele)
positionalControl['values']= ("No attempt", "No", "Yes")
positionalControl.current(0)
positionalControl.grid(column= 13, row= 9, columnspan=5)
positionalControl.config(width= 5)

shooterPosLBL = Label(tele, text='Shooter Position')
shooterPosLBL.grid(column=0, row=8, ipady=23)
shooterPos = ttk.Combobox(tele)
shooterPos['values']= ("A", "B", "C", "D", "E", "F", "G", "H")
shooterPos.current(0)
shooterPos.grid(column= 1, row= 8, columnspan=5)
shooterPos.config(width= 5)
shooterPos.bind("<<ComboboxSelected>>", telePositionSet )

teleTakenLBL = Label(tele, text='Shots Missed')
teleTakenLBL.grid(column=1, row=0, columnspan=5)

teleMadeLBL = Label(tele, text='Shots Made')
teleMadeLBL.grid(column=7, row=0, columnspan=5)

defense_State = BooleanVar(False)
defense = Checkbutton(tele, text='Played Defense?', var=defense_State)
defense.grid(column= 13, row= 10, columnspan=5)


teleEnter = Button(tele, text='enter', command=lambda: sendCycleData(1))
teleEnter.grid(row=8, column=13, ipady=13, ipadx=80)

#End Game

climbingLBL = Label(endGame, text='Climbing')
climbingLBL.grid(column=2, row=0, ipady=10, padx=20)

fellOffBar_State = BooleanVar(False)
fellOffBar = Checkbutton(endGame, text='Fell Off Bar?', var=fellOffBar_State)
fellOffBar.grid(column= 0, row= 1, pady=10)

buddyClimb_State = BooleanVar(False)
buddyClimb = Checkbutton(endGame, text='Buddy Climb?', var=buddyClimb_State)
buddyClimb.grid(column= 3, row= 1, columnspan=4)

hitOpponent_State = BooleanVar(False)
hitOpponent = Checkbutton(endGame, text='Hit Opponent While Climbing?', var=hitOpponent_State)
hitOpponent.grid(column= 0, row= 3, pady=10)

leveledBar_State = BooleanVar(False)
leveledBar = Checkbutton(endGame, text='Leveled the Bar?', var=leveledBar_State)
leveledBar.grid(column= 3, row= 3, columnspan=4)

barLevelLBL = Label(endGame, text='Where was the bar during the climb?')
barLevelLBL.grid(column=0, row=5, ipady=23)
barLevel = ttk.Combobox(endGame)
barLevel['values']= ("Any Position When It Was Leveled", "Middle Of The Bar", "High Side Of The Bar", "Low Side Of The Bar", "No Climb")
barLevel.current(0)
barLevel.grid(column= 3, row= 5, columnspan=6)
barLevel.config(width= 25)

climbFrom = IntVar()
climbFromLBL = Label(endGame, text='Where on the bar did they climb?')
climbFromLBL.grid(column=0, row=7, ipady=23)
barClimb = Radiobutton(endGame, text = 'Bar', value = 1, var=climbFrom)
barClimb.grid(row=7, column=5)
rungClimb = Radiobutton(endGame, text='Rung', value = 2, var=climbFrom)
rungClimb.grid(row=7, column=7)
noClimb = Radiobutton(endGame, text='No climb', value = 0, var=climbFrom)
noClimb.grid(row=7, column=3)

formattingLabel = Label(endGame, text='                                ').grid(row=2, column=2, padx=20)

#Post Match

deadbot_State = BooleanVar(False)
deadbot = Checkbutton(postMatch, text='Deadbot?', var=deadbot_State)
deadbot.grid(column= 0, row= 0)

recoveredFromDead_State = BooleanVar(False)
recoveredFromDead = Checkbutton(postMatch, text='Recovered from dead?', var=recoveredFromDead_State)
recoveredFromDead.grid(column= 2, row= 0)

tippedOver_State = BooleanVar(False)
tippedOver = Checkbutton(postMatch, text='Tipped Over?', var=tippedOver_State)
tippedOver.grid(column= 0, row= 2)

yellowCard_State = BooleanVar(False)
yellowCard = Checkbutton(postMatch, text='Yellow Card?', var=yellowCard_State)
yellowCard.grid(column= 0, row= 3)

redCard_State = BooleanVar(False)
redCard = Checkbutton(postMatch, text='Red Card?', var=redCard_State)
redCard.grid(column= 2, row= 3)

comments= Text(postMatch, width=80, height=4)
comments.grid(column=2, row=4, columnspan=2)
#comments.bind('<Button-1>', popup_keyboard)
commentsLBL = Label(postMatch, text='Comments:')
commentsLBL.grid(column=1, row=4, ipady=21)

dontUseThisData_State = BooleanVar(False)
dontUseThisData = Checkbutton(postMatch, text="Don't use this data", var=dontUseThisData_State)
dontUseThisData.grid(column= 0, row= 5)

#send = Button(postMatch, text='Send to database', command=sendMainData)
#send.grid(row=5, column=2, ipady=13, ipadx=80)
#
#if len(sys.argv) > 1:
#   position = sys.argv[1]
#else:
#   position='R1'
#match_no='2'
#getNextMatch()


window.mainloop()