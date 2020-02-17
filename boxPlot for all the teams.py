# -*- coding: utf-8 -*-
"""
Created on Wed Sep 18 14:33:57 2019

@author: Mason
"""

import pandas as pd
from tkinter import filedialog
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.ticker as ticker

def combineColumn(scoutData): 
    '''
    This combines columns and creates columns from adding other columns. Specifics:
    Total/low/high/outer/inner goal makes/misses/attempts across  game phase(overall)
    Percent of shots are makes, percent of makes in low/high/outer goals, accuracy
    in low and high goal, autonomous score, teleop score.
    '''
    
    scoutData['totalAttempts']=scoutData['lowGoalMissesAuto']+scoutData['highGoalMissesAuto']
    scoutData['totalAttempts']+=scoutData['lowGoalMakesAuto']+scoutData['outerGoalMakesAuto']
    scoutData['totalAttempts']+=scoutData['innerGoalMakesAuto']+scoutData['lowGoalMissesTele']
    scoutData['totalAttempts']+=scoutData['lowGoalMakesTele']+scoutData['outerGoalMakesTele']
    scoutData['totalAttempts']+=scoutData['innerGoalMakesTele']
    
        
    scoutData['lowGoalAttemptsAuto']=scoutData['lowGoalMissesAuto']+scoutData['lowGoalMakesAuto']
    
    scoutData['lowGoalAttemptsTele']=scoutData['lowGoalMissesTele']+scoutData['lowGoalMakesTele']
    
    scoutData['lowGoalAttempts']=scoutData['lowGoalAttemptsAuto']+scoutData['lowGoalAttemptsTele']
    
    scoutData['lowGoalMakes']=scoutData['lowGoalMakesAuto']+scoutData['lowGoalMakesTele']
    
    scoutData['highGoalMakesAuto'] = (scoutData['outerGoalMakesAuto']+scoutData['innerGoalMakesAuto'])
    
    scoutData['highGoalAttemptsAuto']=(scoutData['outerGoalMakesAuto']+scoutData['innerGoalMakesAuto'])+scoutData['highGoalMissesAuto']
    
    scoutData['highGoalAttemptsTele']=(scoutData['outerGoalMakesTele']+scoutData['innerGoalMakesTele'])+scoutData['highGoalMissesTele']
    
    scoutData['highGoalMakesTele']=scoutData['outerGoalMakesTele']+scoutData['innerGoalMakesTele']
    
    scoutData['highGoalAttempts']=scoutData['highGoalAttemptsAuto']+scoutData['highGoalAttemptsTele']

    scoutData['highGoalMakes']=scoutData['outerGoalMakesTele']+scoutData['outerGoalMakesAuto']+scoutData['innerGoalMakesTele']+scoutData['innerGoalMakesAuto']
    
    
    scoutData['outerGoalMakes']=scoutData['outerGoalMakesTele']+scoutData['outerGoalMakesAuto']
    
    
    scoutData['innerGoalMakes']=scoutData['innerGoalMakesAuto']+scoutData['innerGoalMakesTele']

    
    scoutData['totalMakes']=scoutData['innerGoalMakes']+scoutData['outerGoalMakes']+scoutData['lowGoalMakes']
    
    
    scoutData['autoMakes']=scoutData['innerGoalMakesAuto']+scoutData['outerGoalMakesAuto']+scoutData['lowGoalMakesAuto']
    
    
    scoutData['totalAccuracy']=(scoutData['totalMakes']/scoutData['totalAttempts'])*100
    
    scoutData['lowGoalMakesAccuracy']=(scoutData['lowGoalMakes']/scoutData['lowGoalAttempts'])*100
    
    scoutData['lowGoalMakesAccuracyAuto']=(scoutData['lowGoalMakesAuto']/scoutData['lowGoalAttemptsAuto'])*100
    
    scoutData['lowGoalMakesAccuracyTele']=(scoutData['lowGoalMakesTele']/scoutData['lowGoalAttemptsTele'])*100
    
    scoutData['highGoalMakesAccuracy']=(scoutData['highGoalMakes']/scoutData['highGoalAttempts'])*100
    
    scoutData['highGoalMakesAccuracyAuto']=((scoutData['outerGoalMakesAuto']+scoutData['innerGoalMakesAuto'])/scoutData['highGoalAttemptsAuto'])*100
    
    scoutData['highGoalMakesAccuracyTele']=((scoutData['outerGoalMakesTele']+scoutData['innerGoalMakesTele'])/scoutData['highGoalAttemptsTele'])*100
    
    scoutData['percentOfLowGoal']=(scoutData['lowGoalMakes']/scoutData['totalMakes'])*100
    
    scoutData['percentOfOuterGoal']=(scoutData['outerGoalMakes']/scoutData['totalMakes'])*100
    
    scoutData['percentOfInnerGoal']=(scoutData['innerGoalMakes']/scoutData['totalMakes'])*100
    
    
    scoutData['teleopScore']=scoutData['lowGoalMakesTele']+2*scoutData['outerGoalMakesTele']
    scoutData['teleopScore']+=3*scoutData['innerGoalMakesTele']
    
    
    scoutData['autoScore']=2*scoutData['lowGoalMakesAuto']+4*scoutData['outerGoalMakesAuto']
    scoutData['autoScore']+=6*scoutData['innerGoalMakesAuto']
    
    
    scoutData=scoutData.fillna(0)
    
    
#    print(scoutData.head())
    
    return scoutData 

def getPicklistBoxplotData(df, graphVar, title, ax):

    df = df.sort_values('teamNo', ascending=True)
    df = combineColumn(df)
    teamList = df['teamNo'].drop_duplicates()
    df.set_index('teamNo', inplace = True)
    data = []
    dataArr = []
    k=0
    for team in teamList:
        data.append(df.loc[[team], [graphVar]].get_values())
    for i in data:
        dataArr.append([])

        for j in i:
            dataArr[k].append(j[0])
        k+=1
    ax.set_title(title, fontsize=14)
    ax.set_xticklabels(teamList.get_values())
    ax.boxplot(dataArr) 

def getTeamList(df):
    teamList = df['teamNo'].drop_duplicates()
    return(teamList)

def initPicklistGraph(teamList):
   fig = plt.figure(tight_layout=True, figsize=(len(teamList), 10))
   gs = gridspec.GridSpec(3, 1)
   return fig, gs

def initMatchReportGraph():
   fig = plt.figure(tight_layout=True, figsize=(10, 10))
   gs = gridspec.GridSpec(2, 4)
   return fig, gs


def picklistBoxPlots(df):
    fig, gs = initPicklistGraph(getTeamList(df))
    ax1 = fig.add_subplot(gs[0, 0])
    ax2 = fig.add_subplot(gs[1, 0])
    ax3 = fig.add_subplot(gs[2, 0])
    getPicklistBoxplotData(df, 'totalMakes', 'Total Shots Made', ax1)
    getPicklistBoxplotData(df, 'highGoalMakes', 'Total High Shots Made', ax2)
    getPicklistBoxplotData(df, 'autoMakes', 'Total Auto Shots Made', ax3)
    plt.savefig(input('Event name: ') + ' Picklist Graphs')
    plt.show()


def getPrematchScatterPlot(df, team, graphVar, ax):
    ax.scatter(df.loc[[team], ["matchNo"]], df.loc[[team], [graphVar]], color="red")
    ax.set_ylim(top=55, bottom=0)
    ax.xaxis.set_major_locator(ticker.MaxNLocator(integer=True))
    if graphVar == 'autoMakes':
        ax.set_ylim(top=15, bottom=0)
   
    ax.set_title(graphVar)

def cyclePivot(cycleDf, ax, team, graphVar):
    cycleDf.set_index("teamNo", inplace=True)
    

def prematchGraphs(maindf, cycledf, team):
    df = combineColumn(maindf)
    df.set_index("teamNo", inplace = True)
    fig, gs = initMatchReportGraph()
    ax1 = fig.add_subplot(gs[0, 0])
    ax2 = fig.add_subplot(gs[0, 1])
    ax3 = fig.add_subplot(gs[0, 2])
    ax4 = fig.add_subplot(gs[0, 3])
    ax5 = fig.add_subplot(gs[1, 1])
    ax6 = fig.add_subplot(gs[1, 2])
    ax7 = fig.add_subplot(gs[1, 3])
    getPrematchScatterPlot(df, team, 'autoMakes', ax1)
    getPrematchScatterPlot(df, team, 'totalMakes', ax2)
    plt.savefig(str(team) + ' Prematch Graphs')
    plt.show()
    
df = pd.read_csv(filedialog.askopenfilename(title = 'select unfiltered data file'), sep = '|')
#picklistBoxPlots(df)
prematchGraphs(df, 'boo', 2001)