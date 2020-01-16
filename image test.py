# -*- coding: utf-8 -*-
"""
Created on Tue Jan 14 18:10:38 2020

@author: Mason
"""
from tkinter import *
from tkinter import ttk
from tkinter import font
from tkinter import messagebox
import PIL
from PIL import ImageTk, Image

import os


win=Tk()
image = Image.open('Refrence Image.png')
canvas = Canvas(win,width = 800, height = 480)
photo = ImageTk.PhotoImage(image)
canvas.pack(expand=True,fill=BOTH)

#gif1 = PhotoImage(file='C:\\Users\\lnols\\AppData\\Local\\Programs\\Python\\Python37\\test_2.gif')
canvas.create_image(400,240,image=photo)

win.mainloop()

