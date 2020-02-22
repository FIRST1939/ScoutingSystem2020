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

POSMAP = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']

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
            
    '''
    pass

def findfavpos(teamshotsbypos):
    '''

    Parameters
    ----------
    teamshotsbypos : pd.DataFrame
        columns=['teamNo', 'highShots', 'accuracy']

    Returns
    -------
    favdf : pd.DataFrame
        columns = ['teamNo', 'favPos', 'favShots', 'favAcc']
    
    '''
    pass

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
    teamPosShots = maketeamshotsbypos(cycledf)
    teamfavs = findfavpos(teamPosShots)
    teambests = findbestpos(teamPosShots)
    result = joinfavandbest(teamfavs, teambests)
    
    return result
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    