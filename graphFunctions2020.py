# -*- coding: utf-8 -*-
"""
Created on Wed Sep 18 14:33:57 2019

@author: Mason
"""

import pandas as pd
import numpy as np
import seaborn as sb
from tkinter import filedialog
from pprint import pprint
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.ticker as ticker

pd.set_option('display.max_columns', 200)

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

def getPicklistHeatmap(mainDf, df, ax, graphVar):
    df['highGoalMakes'] = df['innerGoalMakes'] + df['outerGoalMakes']
    pprint(df)
    ''' FIX ME VICTORIA
        THE APPEND DOESN'T WORK'''
    mainteams = mainDf['teamNo'].drop_duplicates().to_numpy()
    teams = df['teamNo'].drop_duplicates().to_numpy()

    for team in mainteams:
        if team not in teams:
            #df.append([0, 0, team, 0, 'A', 0, 0, 0, 0, 0, 0])

            newdfentry = pd.DataFrame({'id': [df['id'].max()],'matchNo':[0], 'teamNo':[team], 'cycle':[0], 'shooterPosition':['A'], 'lowGoalMisses':[0],
                                               'highGoalMisses':[0], 'lowGoalMakes':[0], 'outerGoalMakes':[0], 'innerGoalMakes':[0],
                                               'gamePhase':[0], 'highGoalMakes':[0]})
            
            print('\n', newdfentry, '\n')
            
            df = pd.concat([df, newdfentry], ignore_index=True)
            print(team)
 
    print()
    print(df.tail())
    print(df['teamNo'].drop_duplicates())
    
    df = df.sort_values('teamNo', ascending=True)
    highGoalMakesbyMatchDf = getHeatMapPivot(df.loc[:,['matchNo','teamNo','cycle','shooterPosition', graphVar]])
    cookedDf = pd.pivot_table(highGoalMakesbyMatchDf.reset_index().drop(['matchNo'], axis=1), index='teamNo')
    print(cookedDf.stack(1).unstack(level=0))
    yLabels=['A']
    for position in df['shooterPosition'].sort_values().values:
#        print(position)
        passer = False    
        for label in yLabels:
            if label == position:
                passer = True
        if passer == False:
            yLabels.append(position)
    teamList = df['teamNo'].drop_duplicates().to_numpy()
    ax.set_title(graphVar)
    sb.heatmap(cookedDf.stack(1).unstack(level=0).to_numpy(), cmap="YlGn", ax=ax, annot=True, vmin=0, vmax=55, yticklabels=yLabels, xticklabels=teamList )

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

def getClimbHeatMap(mainData, ax):
    mainData['climbCounter'] = 1
    climbData = mainData.set_index('teamNo').loc[:, ['climbLevel', 'climbCounter']]
    climbData = pd.pivot_table(climbData.reset_index(), index=['teamNo', 'climbLevel'], aggfunc=sum)
    climbSums = pd.pivot_table(climbData.reset_index(), index='teamNo', columns= 'climbLevel', aggfunc=sum, margins=True)
    climbSums.fillna(0, inplace=True)
    climbSums.drop('All', inplace=True)
    xLabels = climbSums.index.to_series().values
    climbSums = climbSums.stack(1).unstack(level=0)
    climbSums.drop('No Climb', inplace=True)  
    yLabels = climbSums.index.to_series().values
    sb.heatmap(climbSums.to_numpy(), cmap="YlGn", ax=ax, annot=True, yticklabels=yLabels, xticklabels = xLabels)


def getTeamList(df):
    teamList = df['teamNo'].drop_duplicates()
    return(teamList)

def initPicklistGraph(teamList):
   fig = plt.figure(tight_layout=True, figsize=(len(teamList), 10))
   gs = gridspec.GridSpec(5, 1)
   return fig, gs

def initMatchReportGraph():
   fig = plt.figure(tight_layout=True, figsize=(14, 7))
   gs = gridspec.GridSpec(2, 4)
   return fig, gs


def picklistGraphs(df, cycleDf):
    fig, gs = initPicklistGraph(getTeamList(df))
    ax1 = fig.add_subplot(gs[0, 0])
    ax2 = fig.add_subplot(gs[1, 0])
    ax3 = fig.add_subplot(gs[2, 0])
    ax4 = fig.add_subplot(gs[3, 0])
    ax5 = fig.add_subplot(gs[4, 0])
    getPicklistBoxplotData(df, 'totalMakes', 'Total Shots Made', ax1)
    getPicklistBoxplotData(df, 'highGoalMakes', 'Total High Shots Made', ax2)
    getPicklistBoxplotData(df, 'autoMakes', 'Total Auto Shots Made', ax3)
    getPicklistHeatmap(df, cycleDf, ax4, 'highGoalMakes')
    getClimbHeatMap(df, ax5)
    plt.savefig(input('Event name: ') + ' Picklist Graphs')
    plt.show()


def getPrematchScatterPlot(df, team, graphVar, ax):
    ax.scatter(df.loc[[team], ["matchNo"]], df.loc[[team], [graphVar]], color="red")
    ax.set_ylim(top=55, bottom=0)
    ax.xaxis.set_major_locator(ticker.MaxNLocator(integer=True))
    if graphVar == 'autoMakes':
        ax.set_ylim(top=15, bottom=0)
   
    ax.set_title(graphVar)
    ax.set_xlabel('Matches')
    ax.set_ylabel(graphVar)

  
def getHeatMapPivot(df):
    firstmove = pd.pivot_table(df, index=['matchNo','teamNo','cycle'], columns='shooterPosition',aggfunc=np.sum).fillna(0)
    print(firstmove)
    secondmove = firstmove.groupby(axis=0,level=['matchNo','teamNo'])
    thirdmove = secondmove.sum()
#    print(thirdmove)
    fourthmove = thirdmove.swaplevel(i='matchNo',j='teamNo').sort_index()
#    print(fourthmove)
    return fourthmove    

def getHeatMap(df, mainDf, team, graphVar, ax):
    maxShot =55
    df['highGoalMakes'] = df['innerGoalMakes'] + df['outerGoalMakes']
    df['lowGoalAttempts'] = df['lowGoalMisses'] + df['lowGoalMakes']
    df['highGoalAttempts'] = df['highGoalMisses'] + df['innerGoalMakes'] + df['outerGoalMakes']
    highGoalMakesbyMatchDf = getHeatMapPivot(df.loc[:,['matchNo','teamNo','cycle','shooterPosition', graphVar]])
    yLabels=['A']
    matchNum = []
    for position in df['shooterPosition'].sort_values().values:
        passer = False
        for label in yLabels:
            if label == position:
                passer = True
        if passer == False:
            yLabels.append(position)
    for match in mainDf.set_index('teamNo').loc[[team], ["matchNo"]].values:
        matchNum.append(str(match[0]))
    print(matchNum)
    print(yLabels)
    ax.set_title(graphVar)
    ax.set_xlabel('Matches')
    ax.set_ylabel('Position')
    try: sb.heatmap(highGoalMakesbyMatchDf.loc[[team], :].unstack().stack(1).to_numpy(), cmap="YlGn", ax=ax, annot=True, yticklabels=yLabels, xticklabels=matchNum, vmin=0, vmax=maxShot)
    except:print('data not available')
    
    

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
    getHeatMap(cycledf, maindf, team, 'highGoalAttempts', ax3)
    getHeatMap(cycledf, maindf, team, 'lowGoalAttempts', ax4)
    getHeatMap(cycledf, maindf, team, 'innerGoalMakes', ax5)
    getHeatMap(cycledf, maindf, team, 'outerGoalMakes', ax6)
    getHeatMap(cycledf, maindf, team, 'lowGoalMakes', ax7)
    ax3.title.set_position([.5, 1.2])
    ax4.title.set_position([.5, 1.2])
    ax5.title.set_position([.5, 1.2])
    ax6.title.set_position([.5, 1.2])
    ax7.title.set_position([.5, 1.2])
    plt.savefig(str(team) + ' Prematch Graphs')
    plt.show()
    
maindf = pd.read_csv(filedialog.askopenfilename(title = 'select unfiltered main data file'), sep = '|')
cycledf = pd.read_csv(filedialog.askopenfilename(title = 'select unfiltered cycle data file'), sep = '|')
picklistGraphs(maindf, cycledf)
#prematchGraphs(maindf, cycledf, 1939)
#getPicklistHeatmapPivot(cycledf, 'outerGoalMakes')