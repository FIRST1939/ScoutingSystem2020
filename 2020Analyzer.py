
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 17 19:06:04 2019
                                    
@author: Saketh, Sriram, Charlie
"""

import json
import os
import sys
import tbaUtils
from datetime import datetime
from pprint import pprint
from tkinter import filedialog
from tkinter import *
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.gridspec import GridSpec




#change makeMatchList so the year is the current year using datetime module.
year = datetime.today().year
def makeMatchList(event):
#def makeMatchList(event, year = 2018):

    '''
    Get match list from the Blue Alliance website depending on what event we're 
    going to. Format it and write it to a file. Have that read by the Scouting 
    Program and have formatted so that other scouting software can use it.
    '''
    RawMatches = tbaUtils.get_event_matches(event, year) 

    pprint(RawMatches[0:2])
    
    print()
    MatchList = []
    for Match in RawMatches:
        
        ShortMatch = []
        #Some of these matches are not quals, need to filter out non qm eventually
        MatchNum = Match['match_number']
        ShortMatch.append(MatchNum)
        
        for team in Match['alliances']['blue']['team_keys']:
        
            ShortMatch.append(int(team[3:]))
        
        for team in Match['alliances']['red']['team_keys']:
            
            ShortMatch.append(int(team[3:])) 
            
        comp_level = Match['comp_level']
        if comp_level == 'qm':
            MatchList.append(ShortMatch)
      
    print()
    MatchList.sort()
    pprint(MatchList)    

    with open('MatchList-' + event + '.csv', 'w') as File:
        for Match in MatchList : 
            Outstr = str(Match).replace('[', '').replace(']', '').replace(' ', '')+'\n'
            File.write(Outstr)
            

# #def piecesMath(TeamDf):
#     TeamDf['telecargo'] = TeamDf['teleCargoCargo'] + TeamDf['TeleCargoHRocketCargo'] 
#     TeamDf['telecargo'] += TeamDf['TeleCargoMRocketCargo'] 
#     TeamDf['telecargo'] += TeamDf['TeleCargoLRocketCargo']
  
#     TeamDf['sandcargo'] = TeamDf['SSCargoCargo'] + TeamDf['SSCargoSSHRocketCargo']
#     TeamDf['sandcargo'] += TeamDf['SSCargoSSMRocketCargo']
#     TeamDf['sandcargo'] += TeamDf['SSCargoSSLRocketCargo']

def combineColumn(mainDf): 
    '''
    This combines columns and creates columns from adding other columns. Specifics:
    Total/low/high/outer/inner goal makes/misses/attempts across  game phase(overall)
    Percent of shots are makes, percent of makes in low/high/outer goals, accuracy
    in low and high goal, autonomous score, teleop score.
    '''
    
    mainDf['totalAttempts']=mainDf['lowGoalMissesAuto']+mainDf['highGoalMissesAuto']
    mainDf['totalAttempts']+=mainDf['lowGoalMakesAuto']+mainDf['outerGoalMakesAuto']
    mainDf['totalAttempts']+=mainDf['innerGoalMakesAuto']+mainDf['lowGoalMissesTele']
    mainDf['totalAttempts']+=mainDf['lowGoalMakesTele']+mainDf['outerGoalMakesTele']
    mainDf['totalAttempts']+=mainDf['innerGoalMakesTele']
    
        
    mainDf['lowGoalAttemptsAuto']=mainDf['lowGoalMissesAuto']+mainDf['lowGoalMakesAuto']
    
    mainDf['teleMakes']=mainDf['innerGoalMakesTele']+mainDf['outerGoalMakesTele']+mainDf['lowGoalMakesTele']
    
    mainDf['lowGoalAttemptsTele']=mainDf['lowGoalMissesTele']+mainDf['lowGoalMakesTele']
    
    mainDf['lowGoalAttempts']=mainDf['lowGoalAttemptsAuto']+mainDf['lowGoalAttemptsTele']
    
    mainDf['lowGoalMakes']=mainDf['lowGoalMakesAuto']+mainDf['lowGoalMakesTele']
    
    mainDf['highGoalMakesAuto'] = (mainDf['outerGoalMakesAuto']+mainDf['innerGoalMakesAuto'])
    
    mainDf['highGoalAttemptsAuto']=(mainDf['outerGoalMakesAuto']+mainDf['innerGoalMakesAuto'])+mainDf['highGoalMissesAuto']
    
    mainDf['highGoalAttemptsTele']=(mainDf['outerGoalMakesTele']+mainDf['innerGoalMakesTele'])+mainDf['highGoalMissesTele']
    
    mainDf['highGoalMakesTele']=mainDf['outerGoalMakesTele']+mainDf['innerGoalMakesTele']
    
    mainDf['highGoalAttempts']=mainDf['highGoalAttemptsAuto']+mainDf['highGoalAttemptsTele']

    mainDf['highGoalMakes']=mainDf['outerGoalMakesTele']+mainDf['outerGoalMakesAuto']+mainDf['innerGoalMakesTele']+mainDf['innerGoalMakesAuto']
    
    
    mainDf['outerGoalMakes']=mainDf['outerGoalMakesTele']+mainDf['outerGoalMakesAuto']
    
    
    mainDf['innerGoalMakes']=mainDf['innerGoalMakesAuto']+mainDf['innerGoalMakesTele']

    
    mainDf['totalMakes']=mainDf['innerGoalMakes']+mainDf['outerGoalMakes']+mainDf['lowGoalMakes']
    
    
    mainDf['autoMakes']=mainDf['innerGoalMakesAuto']+mainDf['outerGoalMakesAuto']+mainDf['lowGoalMakesAuto']
    
    #print(mainDf['totalMakes'], mainDf['totalAttempts'])
    mainDf['totalAccuracy']=(mainDf['totalMakes'].astype('int32'))/(mainDf['totalAttempts'].astype('int32'))*100
    
    mainDf['lowGoalMakesAccuracy']=(mainDf['lowGoalMakes']/mainDf['lowGoalAttempts'])*100
    
    mainDf['lowGoalMakesAccuracyAuto']=(mainDf['lowGoalMakesAuto']/mainDf['lowGoalAttemptsAuto'])*100
    
    mainDf['lowGoalMakesAccuracyTele']=(mainDf['lowGoalMakesTele']/mainDf['lowGoalAttemptsTele'])*100
    
    mainDf['highGoalMakesAccuracy']=(mainDf['highGoalMakes']/mainDf['highGoalAttempts'])*100
    
    mainDf['highGoalMakesAccuracyAuto']=((mainDf['outerGoalMakesAuto']+mainDf['innerGoalMakesAuto'])/mainDf['highGoalAttemptsAuto'])*100
    
    mainDf['highGoalMakesAccuracyTele']=((mainDf['outerGoalMakesTele']+mainDf['innerGoalMakesTele'])/mainDf['highGoalAttemptsTele'])*100
    
    mainDf['percentOfLowGoal']=(mainDf['lowGoalMakes']/mainDf['totalMakes'])*100
    
    mainDf['percentOfOuterGoal']=(mainDf['outerGoalMakes']/mainDf['totalMakes'])*100
    
    mainDf['percentOfInnerGoal']=(mainDf['innerGoalMakes']/mainDf['totalMakes'])*100
    
    
    mainDf['teleopScore']=mainDf['lowGoalMakesTele']+2*mainDf['outerGoalMakesTele']
    mainDf['teleopScore']+=3*mainDf['innerGoalMakesTele']
    return mainDf
    
    
def readMatchList():    
    '''
    Read the Match List file created by makeMatchList.     
    
    '''
  #  if testmode : 
   #     FileName = r'C:\Users\Saketh\Documents\GitHub\2019-Scouting-Analyzer\MatchList-nyut.csv'

    FileName = filedialog.askopenfilename(title = 'select MatchList file')
    with open(FileName, 'r') as Matchlist:
       data = Matchlist.readlines()
   
   
    result = []
    for line in data:
        line = line.replace('\n' , '')    
        dataresult = line.split(',')
        for idx in range(len(dataresult)):
            dataresult[idx] = int(dataresult[idx])
        print(dataresult)
        result.append(dataresult)
        
    return result

def whoThis():
    choice = input('who is testing : ')
    return choice
def readScout():
    '''
    Read Scouting Data from a file, fix formatting to numeric where neccessary,
    clean the data, report any implausibile data.  
    '''
   # if testmode :
    #    FileName = r'C:\Users\Saketh\Documents\GitHub\2019-Scouting-Analyzer\MatchScoutForOtherTeams.csv'

    choice = whoThis()
        
    if choice == 'charlie':
        
        mainData = pd.read_csv(r"C:\Users\charl\Downloads\very cool scripts folder\MainData.csv", sep= '|')
        mainDf = mainData.fillna('0')
        
        
        cycleData = pd.read_csv(r"C:\Users\charl\Downloads\very cool scripts folder\CycleData.csv", sep = '|')
        cycleDf = cycleData.fillna('0')
    else:
        
        FileName = filedialog.askopenfilename(title = 'select Main Data file')
        with open(FileName, 'r') as MainFile:
            mainData = pd.read_csv(MainFile, sep = '|') 
        mainDf = mainData.fillna('0')
        
        FileName = filedialog.askopenfilename(title = 'select Cycle Data file')
        with open(FileName, 'r') as CycleFile:
            cycleData = pd.read_csv(CycleFile, sep = '|') 
        cycleDf = cycleData.fillna('0')/"??"""
        
    return mainDf, cycleDf

def readPitScout():
#    FileName = filedialog.askopenfilename(title = 'select pit scouting data file')
#    with open(FileName, 'r') as ScoutFile:
#        pitData = pd.read_csv(ScoutFile, sep = '|') 
#    pitDf = pitData.fillna(value = 0)
    choice = whoThis()
    if choice == 'charlie':
        
        pitDf = pd.read_csv(r'C:\Users\charl\Downloads\very cool scripts folder\PitData.csv', sep= '|')
        pitDf = pitDf.fillna('0')

    else:
        
        FileName = filedialog.askopenfilename(title = 'select Pit Data file')
        with open(FileName, 'r') as PitFile:
            pitDf = pd.read_csv(PitFile, sep = '|') 
        pitDf = pitDf.fillna('0')
    
    return pitDf



    

def FindPartners(Matchlist, team = 1939):    
    '''
    Takes the Match List from the entire competition and finds the matches we're
    in and finds the teams that are with us.
    '''
    result = []
    for match in Matchlist:
        thisMatch = {}
        if team in match[1:]:
         #   print(match)
            if team in match[1:4]:
                thisMatch['alliance'] = 'blue'
                thisMatch['opposing'] = 'red'
                allies = match[1:4]
                thisMatch['opponents'] = match[4:7]
                allies.remove(team)
                thisMatch['allies'] = allies
                
                
            else:
                thisMatch['alliance'] = 'red'
                thisMatch['opposing'] = 'blue'
                allies = match[4:7]
                thisMatch['opponents'] = match[1:4]
                allies.remove(team)
                thisMatch['allies'] = allies
            thisMatch['match'] = match[0] 
            result.append(thisMatch)
            
    return result

            
def MatchReport(MatchList, PivotDf, Scoutdf, TeamNumber):
    ''' (dataframe)->dataframe
    (Scouting Data)->PivotTable with upcoming match partners
    Take the scouting data, trim down to only partners and opponents.
    Create a report by match showing partners and opponents.
    '''
    FileName = 'MatchReport.htm'
    with open(FileName, 'w') as File:
        File.write('<head>\n  <title>Pre-match scouting Report</title><br>\n')
        File.write('<link rel="icon" href="RoboticsAvatar2018.png" />') 
        File.write('<link rel="stylesheet" type="text/css" href="matchrep.css">')
        File.write('</head>\n')
        File.write('<body>\n')
        File.write('<h1><img src="8bit_logo.jpg", width=50, height=60>')
#        File.write('<style>')
#        File.write('img{')
#        File.write('width 100%')
#        File.write('}')
        File.write('</style>')
        File.write('Pre-match scouting Report</h1>\n')
        File.write('<div class="robot">\n')
        File.write('<h3>Our Robot' + '</h3>\n')
        SearchTeam(Scoutdf, PivotDf, TeamNumber, File)

        #print(MatchList[0]['allies'])
        LastScouted = max(Scoutdf['match'])
        
        # Prettying up the file output of the match list
        File.write('<h3>Forthcoming Matches</h3>\n')        
        
        File.write('<table border="1" class="dataframe">\n  <thead>\n    <tr style="text-align: right;">\n')
        File.write('      <th>Match</th>\n')
        File.write('      <th>Alliance</th>\n')
        File.write('      <th>Allies</th>\n')
        File.write('      <th>Opponents</th>\n')
        File.write('    </tr>\n  </thead>\n  <tbody>')

        
        for match in MatchList:
            if match['match'] > LastScouted:
                #File.write(str(match) + '\n')
                File.write('    <tr style="text-align: right;">\n')
                File.write('      <th><a href=#Match' + str(match['match']) + '>' + str(match['match']) + '</a></th>\n')
                File.write('      <th>' + match['alliance'] + '</th>\n')
                File.write('      <th>' + str(match['allies']) + '</th>\n')
                File.write('      <th>' + str(match['opponents']) + '</th>\n')
                File.write('    </tr>\n')                
                File.write('\n')
        File.write('</table>\n')
        File.write('</div>\n')
        #Printing reports for each forthcoming match
        for match in MatchList:
            if match['match'] > LastScouted:
                File.write('<div class="chapter">\n')
                File.write('<a name=Match' + str(match['match']) + '></a>\n')
                File.write('<h2>Match ' + str(match['match']) + '</h2>\n')
                                                               
                #print(len(PivotDf.columns))
                us = [TeamNumber]+match['allies']
                them = match['opponents']                 
                File.write('<h4>'+ match['alliance']+' Alliance</h4>\n')
                if any(i in them for i in PivotDf.index.values):
                    File.write(PivotDf.loc[us].to_html(float_format='{0:.2f}'.format))
                else:
                    File.write('Data not available\n')
                File.write('<h4>'+ match['opposing']+' Alliance</h4>\n')               
                if any(i in them for i in PivotDf.index.values):                    
                    File.write(PivotDf.loc[them].to_html(float_format='{0:.2f}'.format))
                else:
                    File.write('Data not available\n')
                
                File.write('\n<h3>Allies</h3>\n')
                for ally in match['allies']:
                    print(match['allies'])
                    print(ally)
#                    print(match['ally'])
                    SearchTeam(Scoutdf, PivotDf, ally, File)
                    File.write('\n')
                    File.write('<p><img src="G:\\My Drive\\Team 1939 Shared Folder\\Scouting\\Robot Pics\\2019\\Arkansas\\' + str(ally) +'.jpg" style="width:500px;height:600px;"><p>')
                    File.write('\n')
                File.write('\n<h3>Opponents</h3>\n')
                for oppo in match['opponents']:
                    print(match['opponents'])
#                    print(match['oppo'])
                    SearchTeam(Scoutdf, PivotDf, oppo, File)
                    File.write('\n')
                    File.write('<p><img src="G:\\My Drive\\Team 1939 Shared Folder\\Scouting\\Robot Pics\\2019\\Arkansas\\' + str(oppo) +'.jpg" style="width:500px;height:600px;"><p>')
                    File.write('\n')
                File.write('</div>\n')
#                File.write('<p><img src="G:\\My Drive\\Copy of 2019 Pit Scouting (File responses)\\Robot pics\\3937.jpg"><p>')
                ''' with open ('MatchReport.csv', 'w') as File:
                    for match in MatchList:
                    Outstr = str(match)
                    File.write(Outstr)
                    '''
                    
        File.write('</body>\n')    
        
def Day1Report(Scoutdf, PivotDf):
    '''(dataframe)->None
    Take Scouting data and analyze it by creating a report that will be presented
    at the Day 1 Scouting meeting
    '''
    PivotDf.to_csv(r'C:\Users\Mason\Desktop\heatmap analyzed data file.csv')
#    maxScored.to_csv(r'C:\Users\Mason\Desktop\maxScored.csv')
    today = datetime.today().strftime('%Y-%m-%d-%H-%M-%S')
    with pd.DataFrame.ExcelWriter('1st Day report' + str(today) + '.xlsx') as writer:
        Scoutdf = Scoutdf.sort_values(by = 'team')   
        tabname = 'Raw Data'
        Scoutdf.to_excel(writer, tabname, index=False)
        PivotDf = PivotDf.sort_values(by = 'team')
        tabname = 'Data Table'
        PivotDf.to_excel(writer, tabname, index=False)
    print('Day1Report written to file')

def SearchTeam(Scoutdf, PivotDf, TeamNumber, File = None):
    '''
    A Search function where we can find a team and their specific stats.
    '''
    print(Scoutdf)
    if File == None:
        print('Team:', TeamNumber)
        
        if TeamNumber not in PivotDf.team.values:
            print('Team', TeamNumber, 'is not yet scouted')
            return
            
        PivotDf.reset_index(inplace = True)
        PivotDf.set_index('team', inplace = True)
        print('Matches Played =', PivotDf.loc[TeamNumber]['totalmatches'])
        
        print('\nMatch Summary')
        print(PivotDf.loc[TeamNumber].to_dict())
        print('\nMatch Details')
        
        print(Scoutdf[Scoutdf.team == TeamNumber])
    else :
        File.write('<h4>Team: ' + str(TeamNumber) + '</h4>\n')

        PivotDf.reset_index(inplace = True)
                
        if TeamNumber not in PivotDf.team.values:
            File.write('\nTeam ' + str(TeamNumber) + ' is not yet scouted\n')
            PivotDf.set_index('team', inplace = True)
            return
            
        PivotDf.set_index('team', inplace = True)
        File.write('Matches Played =' + str(PivotDf.loc[TeamNumber]['totalmatches']) + '\n')
        
        File.write('\n<h5>Match Summary</h5>\n')
        temp = PivotDf.loc[TeamNumber].to_dict()
        if 'index' in temp:
            del temp['index']
        File.write(str(temp))
        File.write('\n<h5>Match Details</h5>\n')
        
        # Make pandas stop truncating the long text fields.
        pd.set_option('display.max_colwidth', -1)
        
        # Within each write, I'm specifying columns by number, taking off the
        # decimal places, and suppressing printing of the index number

        
        # Comments        
        File.write(Scoutdf[Scoutdf.team == TeamNumber].to_html(columns=['match', 'team', 'Comments', 'scoutName'], float_format='{0:.0f}'.format, index=False, justify='unset'))
        File.write('\n<br>\n')       
        
        #Start Position things
        File.write(Scoutdf[Scoutdf.team == TeamNumber].to_html(columns=['match', 'team', 'startPOS', 'startLeft', 'startRight'], float_format='{0:.0f}'.format, index=False, justify='unset'))
        File.write('\n<br>\n')
        
        # Calculated Fields
        File.write(Scoutdf[Scoutdf.team == TeamNumber].to_html(columns=['match', 'team', 'sandcargo', 'sandhatch', 'telecargo', 'telehatch'], float_format='{0:.0f}'.format, index=False))
        File.write('\n<br>\n')  
        
        # Sandstorm columns
        # Good Stuff
        File.write(Scoutdf[Scoutdf.team == TeamNumber].to_html(columns=['match', 'team', 'SSCargoSSMRocketCargo', 'SSCargoSSLRocketCargo', 'SSCargoSSHRocketHatch', 'SSCargoSSMRocketHatch', 'SSCargoSSLRocketHatch'], float_format='{0:.0f}'.format, index=False))
        File.write('\n<br>\n')
        
        #Failed Stuff
        #File.write(Scoutdf[Scoutdf.team == TeamNumber].to_html(columns=[1, 2, 3, 5, 9, 13], float_format='{0:.0f}'.format, index=False))
        #File.write('\n<br>\n')
        
        
        # Teleop Columns
        # Cube Moving
        File.write(Scoutdf[Scoutdf.team == TeamNumber].to_html(columns=['match', 'team', 'TeleHatchLRocketHatch', 'TeleHatchMRocketHatch', 'TeleHatchHRocketHatch', 'TeleCargoLRocketCargo', 'TeleCargoMRocketCargo', 'TeleCargoHRocketCargo'], float_format='{0:.0f}'.format, index=False))
        File.write('\n<br>\n')
        
        # Climbing and Parking
        File.write(Scoutdf[Scoutdf.team == TeamNumber].to_html(columns=['match', 'team', 'attemptLvl1', 'reachLvl1', 'attemptLvl2', 'reachLvl2', 'attemptLvl3', 'reachLvl3'], float_format='{0:.0f}'.format, index=False))
        File.write('\n<br>\n')
        
        # Ramp and Lift climbing
        File.write(Scoutdf[Scoutdf.team == TeamNumber].to_html(columns=['match', 'team', 'deployedRamps', 'attemptDeployedRamps', 'usedAnotherRobot', 'lift', 'attemptLift'], float_format='{0:.0f}'.format, index=False))
        File.write('\n<br>\n')
        
        
        # Bad Stuff
        File.write(Scoutdf[Scoutdf.team == TeamNumber].to_html(columns=['match', 'team', 'dangerousSSDriving', 'deadbot', 'techFoul', 'foul'], float_format='{0:.0f}'.format, index=False))
        File.write('\n<br>\n')
        
        # Other Stuff
        File.write(Scoutdf[Scoutdf.team == TeamNumber].to_html(columns=['match', 'team', 'crossHABLine', 'defense', 'noAttempt', 'groundPickup', 'touchedRocketLate'], float_format='{0:.0f}'.format, index=False))
        File.write('\n<br>\n')
        
\
                       

# #def TeamStats(TeamDf):
#     '''
#     Takes full dataframe, and creates per match calculated values. Creates a pivot
#     dataframe with overall team statistics
#     '''
#     # Normalize column names
#     # Database renamed match and team to matchNo and teamNo.  We put back.
#     TeamDf.rename(columns = {'teamNo':'team', 'matchNo': 'match'}, inplace = True)
    
#     # Calculate cube usage
#     TeamDf['telecargo'] = TeamDf['teleCargoCargo'] + TeamDf['TeleCargoHRocketCargo'] 
#     TeamDf['telecargo'] += TeamDf['TeleCargoMRocketCargo'] 
#     TeamDf['telecargo'] += TeamDf['TeleCargoLRocketCargo']
  
#     TeamDf['sandcargo'] = TeamDf['SSCargoCargo'] + TeamDf['SSCargoSSHRocketCargo']
#     TeamDf['sandcargo'] += TeamDf['SSCargoSSMRocketCargo']
#     TeamDf['sandcargo'] += TeamDf['SSCargoSSLRocketCargo']
    
#     TeamDf['telehatch'] = TeamDf['teleCargoHatch'] + TeamDf['TeleHatchHRocketHatch']
#     TeamDf['telehatch'] += TeamDf['TeleHatchMRocketHatch']
#     TeamDf['telehatch'] += TeamDf['TeleHatchLRocketHatch']
    
#     TeamDf['sandhatch'] = TeamDf['SSCargoHatch'] + TeamDf['SSCargoSSHRocketHatch']
#     TeamDf['sandhatch'] += TeamDf['SSCargoSSMRocketHatch']
#     TeamDf['sandhatch'] += TeamDf['SSCargoSSLRocketHatch']
    
#     TeamDf['totalscored'] = TeamDf['telecargo'] + TeamDf['sandcargo']
#     TeamDf['totalscored'] += TeamDf['telehatch']
#     TeamDf['totalscored'] += TeamDf['sandhatch']
    
#     TeamDf['teleMakes'] = TeamDf['telecargo'] + TeamDf['telehatch']
    
#     TeamDf['sandTotal'] = TeamDf['sandcargo'] + TeamDf['sandhatch'] 
    
#     tempDf = TeamDf[['team', 'reachLvl1','reachLvl2','reachLvl3', 'defense']]
#     climbDf = pd.pivot_table(tempDf,values=['reachLvl1','reachLvl2','reachLvl3', 'defense'],index=['team'],
#                              columns=['reachLvl1', 'reachLvl2', 'reachLvl3', 'defense'], aggfunc=len, fill_value=0)
#     print(climbDf)
#     climbDf.reset_index(inplace = True)
    
#     #TeamDf['PostiveComments'] = TeamDf['postCommentsPro'] 
    
#     TeamDf['totalmatches'] = 1
    
# #    maxScored = pd.pivot_table(TeamDf, values = ['totalscored'], index='team', aggfunc = TeamDf.loc[[team]].max())
#     AvgTeamPivot = pd.pivot_table(TeamDf, values = ['telecargo', 'sandcargo', 'telehatch', 'sandhatch', 'totalscored'], index = 'team', aggfunc = np.average)
#     MatchCount = pd.pivot_table(TeamDf, values = ['totalmatches', 'reachLvl1', 'reachLvl2', 'reachLvl3', 'defense'], index = 'team', aggfunc = np.count_nonzero)
#     Comments = pd.pivot_table(TeamDf, values = ['Comments'], index = 'team', aggfunc = lambda x: ' '.join(x))
    
#     AvgTeamPivot.reset_index(inplace = True)
#     MatchCount.reset_index(inplace = True)
#     Comments.reset_index(inplace = True)
                                                                               
#     TeamPivot = pd.merge(AvgTeamPivot, MatchCount, on = 'team')
    
#     TeamPivot = pd.merge(TeamPivot, climbDf, on = 'team')
    
    
#     TeamPivot.rename(columns = {"Did not Try": 'noAttempt', "Attempt Level One Climb": 'attemptLvl1', 
#                                 "Climbed Level One": 'reachLvl1', "Attempt Level Two Climb": 'attemptLvl2',
#                                 "Climbed Level Two": 'reachLvl2', "Attempt Level Three Climb": 'attemptLvl3',
#                                 "Climbed Level Three": 'reachLvl3', "Deployed Ramps": 'deployedRamps', 
#                                 "Attempted Deploying Ramps": 'attemptDeployedRamps', "Used Another Robot": 'usedAnotherRobot',
#                                 "Lifted Another Robot": 'lift', "Attempted Lifting Another Robot": 'attemptLift'}, inplace = True)
    
#     return TeamDf, TeamPivot
    

# def PickListCargo(TeamDf, PivotDf, lastMatch):
#     '''
#     List of teams organized by the order we should pick them. Then catagories 
#     that rank robotics based on that catagory. Do not pick catagory.
#     '''
#     earlyDf = TeamDf[TeamDf.match <= lastMatch]
#     lateDf = TeamDf[TeamDf.match > lastMatch]
        
    
#     earlytelepivot = pd.pivot_table(earlyDf, values = ['telecargo'], index = 'team', aggfunc = np.average)
#     latetelepivot = pd.pivot_table(lateDf, values = ['telecargo'], index = 'team', aggfunc = np.average)
    
#     earlytelepivot.reset_index(inplace = True)
#     latetelepivot.reset_index(inplace = True)
#     print(PivotDf.head())
#     deltaDf = pd.merge(earlytelepivot, latetelepivot, on = 'team', suffixes = ('_early', '_late'))
    
    
#     deltaDf['change'] = deltaDf['telecargo_late'] - deltaDf['telecargo_early']
#     deltaDf.sort_values('change')  
    
#    # deltaDf['HatchChange'] = deltaDf['avgtelehatch_late'] - deltaDf['avgtelehatch_early']
#    # deltaDf.sort_values('HatchChange')
    
#     outfile = 'PicklistCargo.xlsx'
#     with ExcelWriter(outfile) as writer:
#         TeamDf = deltaDf.sort_values(by = 'team')   
#         tabname = 'Raw Data'
#         TeamDf.to_excel(writer, tabname, index=False)
#         PivotDf = deltaDf.sort_values(by = ['team'])
#         tabname = 'Pivot'
#         PivotDf.to_excel(writer, tabname, index=False)
#         tabname = 'Changes'
#         deltaDf.to_excel(writer, tabname)
        
# def PickListHatch(TeamDf, PivotDf, lastMatch):
#     '''
#     List of teams organized by the order we should pick them. Then catagories 
#     that rank robotics based on that catagory. Do not pick catagory.
#     '''
#     earlyDf = TeamDf[TeamDf.match <= lastMatch]
#     lateDf = TeamDf[TeamDf.match > lastMatch]
        

#     earlytelepivot = pd.pivot_table(earlyDf, values = ['telehatch'], index = 'team', aggfunc = np.average)
#     latetelepivot = pd.pivot_table(lateDf, values = ['telehatch'], index = 'team', aggfunc = np.average)
    
#     earlytelepivot.reset_index(inplace = True)
#     latetelepivot.reset_index(inplace = True)
#     print(PivotDf.head())
#     deltaDf = pd.merge(earlytelepivot, latetelepivot, on = 'team', suffixes = ('_early', '_late'))
    
    
#     deltaDf['change'] = deltaDf['telehatch_late'] - deltaDf['telehatch_early']
#     deltaDf.sort_values('change')  
    
    
#     outfile = 'PicklistHatch.xlsx'
#     with ExcelWriter(outfile) as writer:
#         TeamDf = deltaDf.sort_values(by = 'team')   
#         tabname = 'Raw Data'
#         TeamDf.to_excel(writer, tabname, index=False)
#         PivotDf = deltaDf.sort_values(by = ['team'])
#         tabname = 'Pivot'
#         PivotDf.to_excel(writer, tabname, index=False)
#         tabname = 'Changes'
#         deltaDf.to_excel(writer, tabname)

     
def enterTeam():
     Team = input('enter team number: ')
     if Team.isdigit():
        Team = int(Team)
        return Team
     else:
        print('input error')
        return

def getTeamScatterplot(team, df):
#    team = int(input('Enter Which Team you want to generate a graph for:'))
#    print('Enter 0 to generate a total pieces graph')
#    print('Enter 1 to generate a sandstorm graph')
#    print('Enter 2 to generate a tele graph')
#    selection = input('Enter your selection here: ')

#    df = pd.read_csv(filedialog.askopenfilename(title = 'select unfiltered data file'), sep = '|')
    df.set_index("teamNo", inplace = True)

    #piecesMath(df)

    print(df.loc[[team], ["matchNo"]])

#    if selection == "0":
    plt.figure()
    
    plt.subplots(sharey = 'col')

    plt.subplot(311)
    plt.title('Total Pieces')
    plt.scatter(df.loc[[team], ["matchNo"]], df.loc[[team], ["totalscored"]])
    plt.ylabel('Total Objects')
    
    plt.subplot(312)
#    plt.title('Total Cargo')
    plt.scatter(df.loc[[team], ["matchNo"]], df.loc[[team], ["totalcargo"]], color="green")
    plt.ylabel('Cargo')

    plt.subplot(313)
#    plt.title('Total Hatch')
    plt.scatter(df.loc[[team], ["matchNo"]], df.loc[[team], ["totalhatch"]], color="red")
    plt.ylabel('HP')
#    plt.savefig(r'/Users/Mason/Desktop/heatmap.pdf')
    
#    if selection == "1":
    plt.figure()
    plt.subplots(sharey = 'col')
    
    plt.subplot(311)
    plt.title('Total Sand')
    plt.scatter(df.loc[[team], ["matchNo"]], df.loc[[team], ["sandtotal"]])
    plt.ylabel('Total Objects')
    
    plt.subplot(312)
#    plt.title('Total Sand Cargo')
    plt.scatter(df.loc[[team], ["matchNo"]], df.loc[[team], ["sandcargo"]], color="green")
    plt.ylabel('Cargo')

    plt.subplot(313)
#    plt.title('Total Sand Hatch')
    plt.scatter(df.loc[[team], ["matchNo"]], df.loc[[team], ["sandhatch"]], color="red")
    plt.ylabel('HP')

#    if selection == "2":
    plt.figure()
    plt.subplots(sharey = 'col')

    plt.subplot(311)
    plt.title('Total Tele Pieces')
    plt.scatter(df.loc[[team], ["matchNo"]], df.loc[[team], ["teleMakes"]])
    plt.ylabel('Total Objects')
    
    plt.subplot(312)
#    plt.title('Total Tele Cargo')
    plt.scatter(df.loc[[team], ["matchNo"]], df.loc[[team], ["telecargo"]], color="green")
    plt.ylabel('Cargo')

    plt.subplot(313)
#    plt.title('Total Tele Hatch')
    plt.scatter(df.loc[[team], ["matchNo"]], df.loc[[team], ["telehatch"]], color="red")
    plt.ylabel('HP')



def getDfTeamList(df):
    return(df['teamNo'].drop_duplicates())

def getPicklistBoxplot(df, yvars, teamList):
    df = df.sort_values('teamNo', ascending=True)
    df.set_index('teamNo', inplace = True)
    data = []
    dataArr = []
    k=0
    for team in teamList:
        data.append(df.loc[[team], [yvars]].get_values())

    for i in data:
        dataArr.append([])
        for j in i:
            dataArr[k].append(j[0])
    return(dataArr)#.set_xticklabels(teamList.get_values()))
def getFirstDayReportExcel(mainDf):
    
#    cycleDf = mainDf[1]
#    pitDf = readPitScout()
    combineColumn(mainDf)
    mainDf_avgpivot = pd.pivot_table(mainDf, index= ['teamNo'], values=['totalMakes', 'autoMakes', 'teleMakes'], aggfunc=np.average)
    mainDf_min = pd.pivot_table(mainDf, index=['teamNo'], values=['totalMakes'], aggfunc=min)
    mainDf_max = pd.pivot_table(mainDf, index=['teamNo'], values=['totalMakes'], aggfunc=max)
    mainDf_nonzerocount = pd.pivot_table(mainDf, index=['teamNo'], values=['matchNo', 'defense', 'cards'], aggfunc=np.count_nonzero)
    
    merged = [mainDf_avgpivot,mainDf_min,mainDf_max,mainDf_nonzerocount]
    mergedDf = pd.concat(merged, axis=1)
    today = datetime.today().strftime('%Y-%m-%d-%H-%M-%S')
    filename = 'merged mainDf' + str(today) + '.xlsx'
    mergedDf.to_excel(filename, sheet_name= 'merged mainDf', index=True)
    path = os.path.abspath(filename)
    directory = os.path.dirname(path)
    print('saved in  ' + str(directory))
    


def getPrematchReportDf(mainDf, cycleDf, pitDf):
    """
    1. Matches Scouted - matchscouted
    2. Average Powercells Scored - avgpcs
    3. Avg High Powercells Scored: avghi
    4. Best Shooting Position:*
    5. Shots Taken There:*
    6. Accuracy There:*
    7. favorite Shooting Position:*
    8. Shots Taken There:*
    9. Accuracy There:*
    10. Tall or Short Bot: bhdf
    11. Drivetrain: dtdf
    12. Times Completed Rotational Control: tcrcdf
    13. Times Completed Positional Control: tcpcdf
    14. Matches Played on Defense: mpod
    * = from cycle data
    10 & 11 are from pit data
    index = team
    """
    
    mainDf = combineColumn(mainDf)
    
    
    #teamList = mainDf['teamNo']
    
    matchscouted = pd.pivot_table(mainDf, values=['matchNo'], aggfunc=np.count_nonzero, index=['teamNo'])
    mslist = matchscouted['matchNo']
    #pprint(matchscouted)
    
    avgpcs = pd.pivot_table(mainDf, values=['totalMakes'], aggfunc=np.average, index=['teamNo'])
    avgpcslis = avgpcs['totalMakes']
    #pprint(avgpcs)
    
    avghi = pd.pivot_table(mainDf, values=['highGoalMakes'], aggfunc=np.average, index=['teamNo'])
    avghils = avghi['highGoalMakes']
    #pprint(avghi)
    
    botheight = pitDf['Tall or Short bot?']
    teamList = mainDf['teamNo']
    pitTeamList = pitDf['Team number of team you are scouting']

    #bottype = pd.pivot_table(pitDf, columns = ['Tall or Short bot?'], index = ['Team number of team you are scouting'])
    heightdict = {'teamNo' : pitTeamList, 'bot height' : botheight}
    bhdf = pd.DataFrame(data=heightdict)
    bhlist = bhdf['bot height']
    #pprint(botheightdf)
    
    drivetrain = pitDf['What drivetrain do they have?']
    dtdict = {'teamNo' : pitTeamList, 'drivetrain' : drivetrain}
    dtdf = pd.DataFrame(data=dtdict)
    dtls = dtdf['drivetrain']
    
    tcrcdf = pd.pivot_table(mainDf, values=['rotationalControl'], aggfunc = np.count_nonzero, index = ['teamNo'])
    #pprint(tcrcdf)
    tcrcls= tcrcdf['rotationalControl']
    tcpcdf = pd.pivot_table(mainDf, values=['positionalControl'], aggfunc = np.count_nonzero, index = ['teamNo'])
    #pprint(tcpcdf)
    tcpcls = tcpcdf['positionalControl']
    mpod = pd.pivot_table(mainDf, values=['defense'], aggfunc = np.count_nonzero, index = ['teamNo'])
    #pprint(mpod)
    mpodls = mpod['defense']
    
    #ultralist = [matchscouted, avgpcs, avghi, tcrcdf, tcpcdf, mpod, dtdf, bhdf]
    
#    stg1 = mainDf.join(matchscouted, how='outer', lsuffix='_left', rsuffix='_right')
#    stg2 = stg1.join(avgpcs, how='outer', lsuffix='_left', rsuffix='_right')
#    stg3 = stg2.join(avghi, how='outer', lsuffix='_left', rsuffix='_right')
#    stg4 = stg3.join(tcrcdf, how='outer', lsuffix='_left', rsuffix='_right')
#    stg5 = stg4.join(tcpcdf, how='outer', lsuffix='_left', rsuffix='_right')
#    stg6 = stg5.join(dtdf, how='outer', lsuffix='_left', rsuffix='_right')
#    ultradf = stg6.join(bhdf, how='outer', lsuffix='_left', rsuffix='_right')
    
    ultraList = {'Matches Scouted' : mslist, 'Average Pieces Scored' : avgpcslis, 'Average High Goal Makes' : avghils, 'Times Completed Rotation Control' : tcrcls, 'Times Completed Positional Control' : tcpcls, 'Matches Played on Defense' : mpodls}
    
    ultraDf = pd.DataFrame(data=ultraList)
    
    ultraDf = ultraDf.fillna('no data')
    
    
    pitultradf = bhdf.merge(dtdf)
    pitultradf.set_index('teamNo', inplace=True)
    
    pitultradf.sort_index(ascending=True)
    ultraDf.sort_index(ascending=True)
    
    prematchScoutingReportDf = ultraDf.merge(pitultradf, on='teamNo')
    today = datetime.today().strftime('%Y-%m-%d-%H-%M-%S')
    pprint(prematchScoutingReportDf)
    prematchScoutingReportDf.to_excel('prematch scouting report' + str(today) + '.xlsx')
    return prematchScoutingReportDf

def getThatExcel(df):
    
    df.to_excel('export' + str(today) + '.xlsx')
    
def Main(testmode):
    print('press 1 to acquire a Match List')
    print('press 2 to get a prematch Scouting Report')
    print('press 3 to get a single team report')
    print('press 4 to get the Day 1 Match Report')
    print('press 5 to get a cargo picklist for Day 2')
    print('press 6 to get a hatch picklist for Day 2')
    print('press 9 for functional math test')
    print('press C to run getFirstDayREportExcel')
    selection = input('enter number: ')
    selection = selection.lower()
    if selection == '1':
        event = input('enter event code: ')
        makeMatchList(event)
        
    elif selection == '2':
        # Team = enterTeam()       
        MainData, CycleData = readScout()
        pitDf = readPitScout()
        # MatchList = readMatchList()
        # #TeamDf, PivotDf = TeamStats(MainData)
        # Partners = FindPartners(MatchList, Team)
        # #matchNum = FindPartners(MatchList, Team)
        # #MatchReport(Partners, PivotDf, TeamDf, Team)
        
    elif selection == '3':
        Team = int(enterTeam())       
        ReadData = readScout()
        # df = ReadData
        # print(ReadData)
        MatchList = readMatchList()
        #TeamDf, PivotDf = TeamStats(ReadData)
        #print (TeamStats(ReadData))
        #SearchTeam(TeamDf, PivotDf, Team)
        #print(df)
        #getTeamScatterplot(Team, df)
    elif selection == '4':
        ReadData = readScout()
        #TeamDf, PivotDf = TeamStats(ReadData)
        print()
        #Day1Report(TeamDf, PivotDf)
    elif selection == '5':
        ReadData = readScout()
        #TeamDf, PivotDf = TeamStats(ReadData)
        lastMatch = int(input('enter last match of Day 1'))
        print('boo')
        #print(TeamDf.head())
        #PickListCargo(TeamDf, PivotDf, lastMatch)
    elif selection == '6':
        ReadData = readScout()
        #TeamDf, PivotDf = TeamStats(ReadData)
        #lastMatch = int(input('enter last match of Day 1'))
        print('boo')
        #print(TeamDf.head())
        #PickListHatch(TeamDf, PivotDf, lastMatch)
    elif selection == '9':

        ReadData = readScout()

        #print('entered 9')
        maindf, cycledf = readScout()
        #print('readFile')
        combinedMaindf=combineColumn(maindf)
        print(combinedMaindf)
        

        #print(ReadData)
        #TeamDf, PivotDf = TeamStats(ReadData)
        
        print()
        print('TeamDF')
        #print(TeamDf)
        print('\nTeam Pivot')
        #print(PivotDf)
    elif selection == 'c':
        Main, Cycle = readScout()
        Pit = readPitScout()
        getPrematchReportDf(Main, Cycle, Pit)
Main(True)
