# -*- coding: utf-8 -*-
"""
Created on Fri Feb 21 22:43:58 2020

@author: Victoria

for the best and favorite position can I pass you the cycle df with all the 
columns it comes out of the database and with the math columns:
high goal makes
high goal shots taken
and then can you return a dataframe with teamNo as the index,
the position where they have the highest high goal accuracy, 
the number of shots they took there total, 
the accuracy there
the position where they have taken the most shots at the high goal
the number of shots they took there total
the accuracy there

for the teams that can't/haven't done high goal, can you just make it so they have 0's for the numbers and their position is "no high goal shots taken"
"""
import pandas as pd
pd.set_option('display.max_columns', 500)
pd.options.display.width = 200
from pprint import pprint
import numpy as np

def maketeamshotsbypos(cycledf):
    '''

    Parameters
    ----------
    cycledf : pd.DataFrame
        Contains cycle data from database and math columns for high goal makes and shots taken.

    Returns
    -------
    teamshotsbypos: pd.DataFrame
        columns=['teamNo', 'highShots', 'accuracy']
        
        the highshots and accuracy columns each contain a list of numbers
        with values from each position
    posmap: list of str
        contains list of positions from which a team has shot for later use            

    
    '''    
    posPivot = pd.pivot_table(cycledf, values=['highGoalMisses','highGoalMakes','highGoalShots'],
                              index=['teamNo', 'shooterPosition'])
    
    posPivot.reset_index(inplace = True)
    
    posPivot['accuracy'] = posPivot['highGoalMakes'] / posPivot['highGoalShots']
    
    highShots = pd.pivot_table(posPivot, values = 'highGoalMakes', index = 'teamNo', columns = 'shooterPosition').fillna(0)
    highShotdict = highShots.to_dict(orient='split')
    posmap = highShotdict['columns']
    print(highShotdict)
    reconfigHigh = pd.Series(highShotdict['data'], index=highShotdict['index']).reset_index(name='highShots').rename(columns={'index': 'teamNo'})
    
    acc = pd.pivot_table(posPivot, values = 'accuracy', index = 'teamNo', columns = 'shooterPosition').fillna(0)
    accdict = acc.to_dict(orient='split')
    reconfigacc = pd.Series(accdict['data'], index=accdict['index']).reset_index(name='accuracy').rename(columns={'index': 'teamNo'})
    
    result = pd.merge(reconfigHigh, reconfigacc, on='teamNo')
    
    
    return result, posmap

def findfavpos(teamshotsbypos, posmap):
    '''

    Parameters
    ----------
    teamshotsbypos : pd.DataFrame
        columns=['teamNo', 'highShots', 'accuracy']
    posmap: list of str
        contains list of positions from which a team has shot

    Returns
    -------
    favdf : pd.DataFrame
        columns = ['teamNo', 'favPos', 'favShots', 'favAcc']
    
    '''
    print(teamshotsbypos['highShots'])
    #teamshotsbypos['favPos'] = np.argmax(teamshotsbypos['highShots'].tolist())
    
    favlist = []
    shotlist = []
    
    # This is a terrible way of going about this
    for item in teamshotsbypos['highShots'].tolist():
        favlist.append(posmap[np.argmax(item)])
        shotlist.append(np.max(item))
    
    teamshotsbypos['favPos'] = favlist
    teamshotsbypos['favShots'] = shotlist
    
    print(teamshotsbypos.head())
    
                                                    

def findbestpos(teamshotsbypos):
    '''
    Parameters
    ----------
    teamshotsbypos : pd.DataFrame
        Contains cycle data from database and math columns for high goal makes and shots taken.

    Returns
    -------
    bestdf : pd.DataFrame
        columns = ['teamNo', 'bestPos', 'bestShots', 'bestAcc']

    '''
    pass

def joinfavandbest(favdf, bestdf):
    '''
    Parameters
    ----------
    favdf : pd.DataFrame
        columns = ['teamNo', 'favPos', 'favShots', 'favAcc']
    bestdf : pd.DataFrame
        columns = ['teamNo', 'bestPos', 'bestShots', 'bestAcc']

    Returns
    -------
    teamprefdf : pd.DataFrame
    
        Join of favdf and bestdf on team

    '''
    pass

def favoritism(cycledf):
    '''
    Parameters
    ----------
    cycledf : pd.DataFrame
        Contains cycle data from database and math columns for high goal makes and shots taken.

    Returns
    -------
    teamprefdf: pd.DataFrame
        columns = ['teamNo', 'favPos', 'favShots', 'favAcc', 'bestPos', 'bestShots', 'bestAcc]

    '''
    print('Starting favorites run')
    teamPosShots, posmap = maketeamshotsbypos(cycledf)
    print(teamPosShots.head())

    teamfavs = findfavpos(teamPosShots, posmap)
    teambests = findbestpos(teamPosShots)
    result = joinfavandbest(teamfavs, teambests)
    
    return result
    
    

#testsample = pd.read_csv(r'C:\Users\stat\Downloads\2020Cycle data with robot types.csv', sep='|')
#pprint(testsample.to_dict(orient='split'))

columns = [ 'id',
            'matchNo',
            'teamNo',
            'cycle',
            'shooterPosition',
            'lowGoalMisses',
            'highGoalMisses',
            'lowGoalMakes',
            'outerGoalMakes',
            'innerGoalMakes',
            'gamePhase',
            'highGoalMakes',
            'highGoalShots']
testdata =  [[1, 1, 1939, 0, 'E', 0, 0, 0, 3, 0, 0, 3, 3],
          [2, 1, 1939, 1, 'A', 0, 1, 0, 4, 0, 1, 4, 5],
          [3, 1, 1939, 2, 'A', 0, 1, 0, 4, 0, 1, 4, 5],
          [4, 1, 1939, 3, 'A', 0, 1, 0, 4, 0, 1, 4, 5],
          [5, 1, 1939, 4, 'A', 0, 1, 0, 4, 0, 1, 4, 5],
          [6, 1, 1939, 5, 'A', 0, 0, 0, 0, 5, 1, 5, 5],
          [7, 1, 1678, 0, 'B', 0, 0, 0, 0, 3, 0, 3, 3],
          [8, 1, 1678, 1, 'A', 0, 0, 0, 0, 5, 0, 5, 5],
          [9, 1, 1678, 0, 'B', 0, 2, 0, 3, 0, 1, 3, 5],
          [10, 1, 1678, 1, 'A', 0, 0, 0, 0, 5, 1, 5, 5],
          [11, 1, 1678, 2, 'A', 0, 0, 0, 0, 5, 1, 5, 5],
          [12, 1, 1678, 3, 'A', 0, 0, 0, 0, 5, 1, 5, 5],
          [13, 1, 1678, 4, 'A', 0, 0, 0, 0, 5, 1, 5, 5],
          [14, 1, 1678, 5, 'A', 0, 0, 0, 0, 5, 1, 5, 5],
          [15, 1, 1678, 6, 'A', 0, 0, 0, 0, 5, 1, 5, 5],
          [16, 1, 1678, 7, 'A', 0, 0, 0, 0, 5, 1, 5, 5],
          [17, 1, 1678, 8, 'A', 0, 0, 0, 0, 5, 1, 5, 5],
          [18, 1, 1678, 9, 'A', 0, 0, 0, 0, 5, 1, 5, 5],
          [19, 1, 5809, 0, 'C', 0, 0, 3, 0, 0, 0, 0, 0],
          [20, 1, 5098, 0, 'C', 1, 0, 2, 0, 0, 0, 0, 0],
          [21, 1, 5006, 0, 'E', 0, 0, 0, 2, 1, 0, 3, 3],
          [22, 1, 5006, 0, 'C', 0, 1, 0, 4, 1, 1, 5, 6],
          [23, 1, 5006, 1, 'C', 0, 0, 0, 4, 1, 1, 5, 5],
          [24, 2, 1939, 0, 'E', 0, 1, 0, 2, 0, 0, 2, 3],
          [25, 2, 1939, 0, 'E', 0, 2, 0, 3, 0, 1, 3, 5],
          [26, 2, 1939, 1, 'E', 0, 2, 0, 3, 0, 1, 3, 5],
          [27, 2, 1939, 2, 'D', 0, 0, 0, 2, 3, 1, 5, 5],
          [28, 2, 1939, 3, 'D', 0, 0, 0, 2, 3, 1, 5, 5],
          [29, 2, 1939, 4, 'D', 0, 0, 0, 2, 3, 1, 5, 5],
          [30, 2, 1678, 0, 'B', 0, 0, 0, 0, 3, 0, 3, 3],
          [31, 2, 1678, 1, 'A', 0, 0, 0, 0, 5, 0, 5, 5],
          [32, 2, 1678, 0, 'B', 0, 2, 0, 3, 0, 1, 3, 5],
          [33, 2, 1678, 1, 'A', 0, 0, 0, 0, 5, 1, 5, 5],
          [34, 2, 1678, 2, 'A', 0, 0, 0, 0, 5, 1, 5, 5],
          [35, 2, 1678, 3, 'A', 0, 0, 0, 0, 5, 1, 5, 5],
          [36, 2, 1678, 4, 'A', 0, 0, 0, 0, 5, 1, 5, 5],
          [37, 2, 1678, 5, 'A', 0, 0, 0, 0, 5, 1, 5, 5],
          [38, 2, 1678, 6, 'A', 0, 0, 0, 0, 5, 1, 5, 5],
          [39, 2, 1678, 7, 'A', 0, 0, 0, 0, 5, 1, 5, 5],
          [40, 2, 1678, 8, 'A', 0, 0, 0, 0, 5, 1, 5, 5],
          [41, 2, 1678, 9, 'A', 0, 0, 0, 0, 5, 1, 5, 5],
          [42, 2, 4959, 0, 'C', 0, 0, 5, 0, 0, 1, 0, 0],
          [43, 2, 4959, 1, 'C', 0, 0, 5, 0, 0, 1, 0, 0],
          [44, 2, 4959, 2, 'C', 0, 0, 5, 0, 0, 1, 0, 0],
          [45, 2, 2001, 0, 'E', 0, 0, 0, 3, 0, 0, 3, 3],
          [46, 2, 2001, 0, 'C', 0, 1, 0, 4, 0, 1, 4, 5],
          [47, 2, 2001, 1, 'C', 0, 1, 0, 4, 0, 1, 4, 5],
          [48, 2, 2001, 2, 'C', 0, 1, 0, 4, 0, 1, 4, 5],
          [49, 2, 4499, 0, 'E', 0, 3, 0, 0, 0, 0, 0, 3],
          [50, 2, 4499, 0, 'A', 0, 1, 0, 4, 0, 1, 4, 5],
          [51, 2, 4499, 1, 'A', 0, 1, 0, 4, 0, 1, 4, 5],
          [52, 2, 4499, 2, 'A', 0, 1, 0, 4, 0, 1, 4, 5],
          [53, 2, 4499, 3, 'A', 0, 0, 0, 3, 2, 1, 5, 5],
          [54, 2, 4499, 4, 'A', 0, 0, 0, 3, 2, 1, 5, 5],
          [55, 2, 4499, 5, 'A', 0, 0, 0, 3, 2, 1, 5, 5],
          [56, 2, 4499, 6, 'A', 0, 0, 0, 3, 2, 1, 5, 5],
          [57, 2, 4499, 7, 'A', 0, 0, 0, 1, 4, 1, 5, 5],
          [58, 3, 1986, 0, 'C', 0, 3, 0, 0, 0, 0, 0, 3],
          [59, 3, 1986, 1, 'C', 0, 3, 0, 2, 0, 1, 2, 5],
          [60, 3, 1986, 2, 'D', 0, 4, 0, 1, 0, 1, 1, 5],
          [61, 3, 1986, 3, 'E', 0, 5, 0, 0, 0, 1, 0, 5],
          [62, 3, 1810, 0, 'D', 0, 0, 0, 3, 0, 0, 3, 3],
          [63, 3, 1810, 1, 'A', 0, 1, 0, 4, 0, 1, 4, 5],
          [64, 3, 1810, 2, 'A', 0, 1, 0, 4, 0, 1, 4, 5],
          [65, 3, 1810, 3, 'A', 0, 2, 0, 3, 0, 1, 3, 5],
          [66, 3, 1810, 4, 'A', 0, 1, 0, 3, 1, 1, 4, 5],
          [67, 3, 1810, 5, 'A', 0, 1, 0, 3, 2, 1, 5, 6],
          [68, 3, 1678, 0, 'B', 0, 0, 0, 0, 3, 0, 3, 3],
          [69, 3, 1678, 1, 'A', 0, 0, 0, 0, 5, 0, 5, 5],
          [70, 3, 1678, 0, 'B', 0, 2, 0, 3, 0, 1, 3, 5],
          [71, 3, 1678, 1, 'A', 0, 0, 0, 0, 5, 1, 5, 5],
          [72, 3, 1678, 2, 'A', 0, 0, 0, 0, 5, 1, 5, 5],
          [73, 3, 1678, 3, 'A', 0, 0, 0, 0, 5, 1, 5, 5],
          [74, 3, 1678, 4, 'A', 0, 0, 0, 0, 5, 1, 5, 5],
          [75, 3, 1678, 5, 'A', 0, 0, 0, 0, 5, 1, 5, 5],
          [76, 3, 1678, 6, 'A', 0, 0, 0, 0, 5, 1, 5, 5],
          [77, 3, 1678, 7, 'A', 0, 0, 0, 0, 5, 1, 5, 5],
          [78, 3, 1678, 8, 'A', 0, 0, 0, 0, 5, 1, 5, 5],
          [79, 3, 1678, 9, 'A', 0, 0, 0, 0, 5, 1, 5, 5],
          [80, 3, 1939, 0, 'E', 0, 0, 0, 2, 1, 0, 3, 3],
          [81, 3, 1939, 0, 'A', 0, 1, 0, 3, 1, 1, 4, 5],
          [82, 3, 1939, 1, 'A', 0, 1, 0, 3, 1, 1, 4, 5],
          [83, 3, 1939, 2, 'A', 0, 1, 0, 3, 1, 1, 4, 5],
          [84, 3, 1939, 3, 'A', 0, 0, 0, 4, 1, 1, 5, 5],
          [85, 3, 1939, 4, 'A', 0, 0, 0, 4, 1, 1, 5, 5],
          [86, 3, 1939, 5, 'A', 0, 0, 0, 4, 1, 1, 5, 5],
          [87, 3, 1939, 6, 'A', 0, 0, 0, 1, 2, 1, 3, 3],
          [88, 3, 1939, 7, 'A', 0, 0, 0, 1, 2, 1, 3, 3],
          [89, 4, 1810, 0, 'B', 0, 3, 0, 0, 0, 0, 0, 3],
          [90, 4, 1810, 1, 'B', 0, 4, 0, 1, 0, 1, 1, 5],
          [91, 4, 1810, 2, 'B', 0, 4, 0, 1, 0, 1, 1, 5],
          [92, 4, 1810, 3, 'B', 0, 4, 0, 1, 0, 1, 1, 5],
          [93, 4, 1810, 4, 'B', 0, 3, 0, 2, 0, 1, 2, 5],
          [94, 4, 1810, 5, 'B', 0, 4, 0, 1, 0, 1, 1, 5],
          [95, 4, 1785, 0, 'B', 0, 3, 0, 0, 0, 0, 0, 3],
          [96, 4, 1785, 1, 'A', 0, 1, 0, 4, 0, 1, 4, 5],
          [97, 4, 1785, 2, 'A', 0, 1, 0, 4, 0, 1, 4, 5],
          [98, 4, 1785, 3, 'A', 0, 1, 0, 4, 0, 1, 4, 5],
          [99, 4, 1785, 4, 'A', 0, 1, 0, 4, 0, 1, 4, 5],
          [100, 4, 1785, 5, 'B', 0, 3, 0, 2, 0, 1, 2, 5],
          [101, 4, 1785, 6, 'B', 0, 3, 0, 2, 0, 1, 2, 5]]

testsample = pd.DataFrame(testdata, columns=columns)
print(testsample.head())
    
favoritism(testsample)    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    