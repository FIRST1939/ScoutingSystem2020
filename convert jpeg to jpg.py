# -*- coding: utf-8 -*-
"""
Created on Mon Feb 24 10:13:30 2020

@author: Mason
"""

from tkinter import filedialog
from glob import glob
import os

fromdir =  filedialog.askdirectory(title='select directory to convert files to jpg')
filelist = glob(os.path.join(fromdir, '*.jpeg'))
for file in filelist:
    fileName = file[:-4] + 'jpg'
    os.replace(file, fileName)