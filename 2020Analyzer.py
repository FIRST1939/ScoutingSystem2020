
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 17 19:06:04 2019
                                    
@author: Saketh, Sriram, Charlie, Mason
"""

import os
import sys
import shutil
from glob import glob
import tbaUtils
from datetime import datetime
from pprint import pprint
from tkinter import filedialog
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sb
import matplotlib.gridspec as gridspec
import matplotlib.ticker as ticker



#change makeMatchList so the year is the current year using datetime module.

year = datetime.today().year


def makeMatchList(event):

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
    if pickedchoice == 'charlie':
           FileName = (r"C:\Users\charl\Downloads\Test data match list - Sheet1.csv")
           
    elif pickedchoice == 'm':
        FileName = (r"C:\Users\Mason\Downloads\Test data match list - Sheet1 (4)")

    else:
       
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

pickedchoice = whoThis()

def readScout():
    '''
    Read Scouting Data from a file, fix formatting to numeric where neccessary,
    clean the data, report any implausibile data.  
    '''
   # if testmode :
    #    FileName = r'C:\Users\Saketh\Documents\GitHub\2019-Scouting-Analyzer\MatchScoutForOtherTeams.csv'


    if pickedchoice == 'charlie':
        
        mainData = pd.read_csv(r"C:\Users\charl\Downloads\very cool scripts folder\MainData.csv", sep= '|')
        mainDf = mainData.fillna('0')
        
        
        cycleData = pd.read_csv(r"C:\Users\charl\Downloads\very cool scripts folder\CycleData.csv", sep = '|')
        cycleDf = cycleData.fillna('0')
        
    elif pickedchoice == 'm':
        mainData = pd.read_csv(r"C:\Users\Mason\Downloads\2020 test data sheet with robot types - Main Data with robot types (1).csv", sep= '|')
        mainDf = mainData.fillna('0')
        
        
        cycleData = pd.read_csv(r"C:\Users\Mason\Downloads\2020 test data sheet with robot types - Cycle data with robot types (1).csv", sep = '|')
        cycleDf = cycleData.fillna('0')
    else:
        
        FileName = filedialog.askopenfilename(title = 'select Main Data file')
        with open(FileName, 'r') as MainFile:
            mainData = pd.read_csv(MainFile, sep = '|') 
        mainDf = mainData.fillna('0')
#        print('pickle rick find me in the code hahaha')
        FileName = filedialog.askopenfilename(title = 'select Cycle Data file')
        with open(FileName, 'r') as CycleFile:
            cycleData = pd.read_csv(CycleFile, sep = '|') 
        cycleDf = cycleData.fillna('0')
        
    return mainDf, cycleDf


def readPitScout():
    
    if pickedchoice == 'charlie':
        
        pitDf = pd.read_csv(r'C:\Users\charl\Downloads\very cool scripts folder\PitData.csv', sep= '|')
        pitDf = pitDf.fillna('0')
        
    elif pickedchoice == 'm':
        pitDf = pd.read_csv(r'C:\Users\Mason\Downloads\Pit Scouting (Responses) - Form Responses 1 (1).csv', sep= ',')
        pitDf = pitDf.fillna('0')

    else:
        
        FileName = filedialog.askopenfilename(title = 'select Pit Data file')
        with open(FileName, 'r') as PitFile:
            pitDf = pd.read_csv(PitFile, sep = ',') 
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
    #print(result['opponents'][0])
    return result
          
def MatchReport(MatchList, cycleDf, mainDf, TeamNumber):
    ''' (dataframe)->dataframe
    (Scouting Data)->PivotTable with upcoming match partners
    Take the scouting data, trim down to only partners and opponents.
    Create a report by match showing partners and opponents.
    '''
    filepath = filedialog.askdirectory(title='select directory for team photos')
    pitDf = readPitScout()
    prematchDf = getPrematchReportDf(mainDf, cycleDf, pitDf)
    mainDf.reset_index().set_index('teamNo', inplace = True)
    save = input('Would you like to save the reports to another folder(y/n)?')
    if save == 'y':
        todir = filedialog.askdirectory(title='select directory to send the files')

    for match in MatchList:
        teams = [int(TeamNumber)]
        teams.extend(match['allies'])
        teams.extend(match['opponents'])
        LastScouted = max(mainDf['matchNo'])
        if match['match'] > LastScouted:
                FileName = 'Match ' + str(match['match']) + ' Pre-match Report.html'
                with open(FileName, 'w') as File:
                        File.write('<html>')
                        
                        File.write('<head>')
                        File.write('<meta name="viewport" content="width=device-width, initial-scale=1">')
                        File.write('<style>')
                        File.write('body {')
                        File.write('  font-family: Arial;')
                        File.write('}')
                        
                        #/* Style the tab */
                        File.write('.tab {')
                        File.write('  overflow: hidden;')
                        File.write('  border: 1px solid #ccc;')
                        File.write('  background-color: #f1f1f1;')
                        File.write('}')
                        
                        #/* Style the buttons inside the tab */
                        File.write('.tab button {')
                        File.write('  background-color: inherit;')
                        File.write('  float: left;')
                        File.write('  border: none;')
                        File.write('  outline: none;')
                        File.write('  cursor: pointer;')
                        File.write('  padding: 14px 16px;')
                        File.write('  transition: 0.3s;')
                        File.write('  font-size: 17px;')
                        File.write('}')
                        
                        #/* Change background color of buttons on hover */
                        File.write('.tab button:hover {')
                        File.write('  background-color: #ddd;')
                        File.write('}')
                        
                        #/* Create an active/current tablink class */
                        File.write('.tab button.active {')
                        File.write('  background-color: #ccc;')
                        File.write('}')
                        
                        #/* Style the tab content */
                        File.write('.tabcontent {')
                        File.write('  display: none;')
                        File.write('  padding: 6px 12px;')
                        File.write('  border: 1px solid #ccc;')
                        File.write('  border-top: none;')
                        File.write('}')
                        File.write('.graphSheet{')
                        File.write('	width: 894px;')
                        File.write('	display: inline-block;')
                        File.write('	vertical-align:top')
                        File.write('}')
                        File.write('.team-card {')
                        File.write('  width: 400px;')
                        File.write('  display: inline-block;')
                        File.write('}')
                        
                        File.write('.team-card-text {')
                        File.write('  padding: 0 40px;')
                        File.write('}')
                        File.write('</style>')

                        File.write('</head>')
                        File.write('<body>')
                        File.write('<h2>Prematch Report</h2>')
                        File.write('<p>Match: ' + str(match['match']) + '</p>')
                        
                        File.write('<div class="tab">')
                        File.write('  <button class="tablinks active" onclick="openTab(event, \'Overview\')">Overview</button>')
                        for team in teams:
                            File.write('<button class="tablinks" onclick="openTab(event, \'' + str(team)+'\')">' + str(team) + '</button>\n')
                        File.write('</div>')   
                        File.write('                        <div id="Overview" class="tabcontent" style="display: block;">')
                        File.write('                        <h3>Overview</h3>')
#                    print(teams)  
                        for team in teams:
                            try:
                                File.write('<div class="team-card">')
                                File.write('      <img src=\"' + os.path.join(filepath, str(team) + '.jpg') + '\" alt="pic not found for team ' + str(team) + '" style="width:350px;height:400px;">')
                                File.write('      <p>Team:' + str(team) + '</p>')
                                File.write('      <p>Matches Scouted: ' + str(prematchDf.at[team, 'Matches Scouted'])+ ' </p>')
                                File.write('      <p>Average Powercells Scored: '+ str(prematchDf.at[team, 'Average Pieces Scored']) + '</p>')
                                File.write('      <p>Avg High Powercells Scored: ' + str(prematchDf.at[team, 'Average High Goal Makes'])+'</p>')
                                File.write('	  <p>Tall or Short Bot: ' + str(prematchDf.at[team, 'bot height']) + '</p>')
                                File.write('	  <p>Drivetrain: ' + str(prematchDf.at[team, 'drivetrain']) + '</p>')
                                File.write('	  <p>Times Completed Rotational Control: ' + str(prematchDf.at[team, 'Times Completed Rotation Control' ]) + '</p>')
                                File.write('	  <p>Times Completed Positional Control: ' + str(prematchDf.at[team,'Times Completed Positional Control' ]) + '</p>')
                                File.write('	  <p>Matches Played on Defense: ' + str(prematchDf.at[team, 'Matches Played on Defense']) +   '</p>')
                                File.write(mainDf.reset_index().set_index('teamNo').loc[[team], ['climbLevel']].to_html(index=False))
                                File.write('</div>')
                                File.write('</div>')
                            except:
                                File.write( str(team) + '\'s data not found')
                        for team in teams:
                            try:
                                prematchGraphs(mainDf.reset_index(), cycleDf.reset_index(), team)                
                                File.write('                            <div id="' + str(team) + '" class="tabcontent">')
                                File.write('  <h3>' + str(team) + '</h3>')
                                File.write('  <div class="team-card">')
                                File.write('      <img src=\"' + os.path.join(filepath, str(team) + '.jpg') + '\" alt="pic not found for team ' + str(team) + '" style="width:350px;height:400px;">')
                                File.write('      <p>Team: ' + str(team) + '</p>')
                                File.write('      <p>Matches Scouted: ' + str(prematchDf.at[team, 'Matches Scouted']) + '</p>')
                                File.write('      <p>Average Powercells Scored: '+ str(prematchDf.at[team, 'Average Pieces Scored']) + '</p>')
                                File.write('      <p>Avg High Powercells Scored: ' + str(prematchDf.at[team, 'Average High Goal Makes'])+'</p>')
                                File.write('	  <p>Tall or Short Bot: ' + str(prematchDf.at[team, 'bot height']) + '</p>')
                                File.write('	  <p>Drivetrain: ' + str(prematchDf.at[team, 'drivetrain']) + '</p>')
                                File.write('	  <p>Times Completed Rotational Control: ' + str(prematchDf.at[team, 'Times Completed Rotation Control' ]) + '</p>')
                                File.write('	  <p>Times Completed Positional Control: ' + str(prematchDf.at[team,'Times Completed Positional Control' ]) + '</p>')
                                File.write('	  <p>Matches Played on Defense: ' + str(prematchDf.at[team, 'Matches Played on Defense']) +   '</p>')
                                File.write(mainDf.reset_index().set_index('teamNo').loc[[team], ['climbLevel']].to_html(index=False))
                                File.write(mainDf.reset_index().set_index('teamNo').loc[[team], ['comments']].to_html(index=False))
                                File.write('  </div>')
                                File.write('  <div class="graphSheet">')
                                File.write('	<img src="./' + str(team) + ' Prematch Graphs.png" alt="graph" style="width:894px">')
                                File.write('  </div>')
                                File.write('</div>')
                            except:
                                File.write('Haha data not found still')
                        File.write('                    <script>')
                        File.write('                    function openTab(evt, tabName) {')
                        File.write('                      var i, tabcontent, tablinks;')
                        File.write('                      tabcontent = document.getElementsByClassName("tabcontent");')
                        File.write('                      for (i = 0; i < tabcontent.length; i++) {')
                        File.write('                        tabcontent[i].style.display = "none";')
                        File.write('                      }')
                        File.write('                      tablinks = document.getElementsByClassName("tablinks");')
                        File.write('                      for (i = 0; i < tablinks.length; i++) {')
                        File.write('                        tablinks[i].className = tablinks[i].className.replace(" active", "");')
                        File.write('                      }')
                        File.write('                      document.getElementById(tabName).style.display = "block";')
                        File.write('                      evt.currentTarget.className += " active";')
                        File.write('                    }')
                        File.write('                    </script>                    ')
                        File.write('                    </body>                    ')
                        File.write('                    </html>')
                        if save == 'y':
                                    shutil.copy('Match ' + str(match['match']) + ' Pre-match Report.html', todir)
                                    for team in teams:        
                                        try: shutil.copy(os.path.join(filepath, str(team) + '.jpg'), todir)
                                        except: print('Photo not Found for ' + str(team))
                                        try: shutil.copy(str(team) + ' Prematch Graphs.png', todir)
                                        except: print('photo not found for ' + str(team))

        
def Day1Report(Scoutdf, PivotDf):
    '''(dataframe)->None
    Take Scouting data and analyze it by creating a report that will be presented
    at the Day 1 Scouting meeting
    '''
    PivotDf.to_csv(r'C:\Users\Mason\Desktop\heatmap analyzed data file.csv')
    #maxScored.to_csv(r'C:\Users\Mason\Desktop\maxScored.csv')
    today = datetime.today().strftime('%Y-%m-%d-%H-%M-%S')
    with pd.DataFrame.ExcelWriter('1st Day report' + str(today) + '.xlsx') as writer:
        Scoutdf = Scoutdf.sort_values(by = 'team')   
        tabname = 'Raw Data'
        Scoutdf.to_excel(writer, tabname, index=False)
        PivotDf = PivotDf.sort_values(by = 'team')
        tabname = 'Data Table'
        PivotDf.to_excel(writer, tabname, index=False)
    print('Day1Report written to file')


def enterTeam():
     Team = input('enter team number: ')
     if Team.isdigit():
        Team = int(Team)
        return Team
     else:
        print('input error')
        return


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
                              index=['teamNo', 'shooterPosition'], aggfunc = np.sum)
    
    posPivot.reset_index(inplace = True)
    
    #print(posPivot.head())
    
    posPivot['accuracy'] = posPivot['highGoalMakes'] / posPivot['highGoalShots']
    
    highShots = pd.pivot_table(posPivot, values = 'highGoalMakes', index = 'teamNo', columns = 'shooterPosition').fillna(0)
    highShotdict = highShots.to_dict(orient='split')
    posmap = highShotdict['columns']
    #print(highShotdict)
    reconfigHigh = pd.Series(highShotdict['data'], index=highShotdict['index']).reset_index(name='highShots').rename(columns={'index': 'teamNo'})
    
    acc = pd.pivot_table(posPivot, values = 'accuracy', index = 'teamNo', columns = 'shooterPosition').fillna(0)
    accdict = acc.to_dict(orient='split')
    reconfigacc = pd.Series(accdict['data'], index=accdict['index']).reset_index(name='accuracy').rename(columns={'index': 'teamNo'})
    
    result = pd.merge(reconfigHigh, reconfigacc, on='teamNo')
    
    
    return result, posmap

def findpos(teamshotsbypos, posmap, mostwhat):
    '''
    Parameters
    ----------
    teamshotsbypos : pd.DataFrame
        columns=['teamNo', 'highShots', 'accuracy']
    posmap: list of str
        contains list of positions from which a team has shot
    mostwhat : str
        field name (of highshots or accuracy) to calculate on

    Returns
    -------
    resultdf : pd.DataFrame
        columns = ['teamNo', 'pos', 'shots', 'acc']

    '''
    
    poslist = []
    shotlist = []
    acclist = []
       
    highshots = teamshotsbypos['highShots'].tolist()
    accs = teamshotsbypos['accuracy'].tolist()
    
    # This is a terrible way of going about this
    for index in range(len(highshots)):
        posidx = np.argmax(teamshotsbypos[mostwhat].tolist()[index])
        poslist.append(posmap[posidx])
        shotlist.append(highshots[index][posidx])
        acclist.append(accs[index][posidx])
    
    teamshotsbypos['pos'] = poslist
    teamshotsbypos['shots'] = shotlist
    teamshotsbypos['acc'] = acclist
    
    #print(teamshotsbypos.head())
    
    return teamshotsbypos[['teamNo', 'pos', 'shots', 'acc']]



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
    return pd.merge(favdf, bestdf, on='teamNo', how='inner', suffixes = ('Most','Best'))

def addmissingteams(df, teamlist):
    '''
    

    Parameters
    ----------
    df : pd.DataFrame
        columns = ['teamNo', 'posMost', 'shotsMost', 'accMost', 'posBest', 'shotsBest', 'accBest']
    teamlist : list of int
        list of all teams at the regional

    Returns
    -------
    result : pd.DataFrame
        df but with lines added for teams with no cycle data

    '''
    
    cycleteams = df['teamNo'].drop_duplicates().tolist()
    
    
    for team in teamlist:
        if team not in cycleteams:
            nulldf = pd.DataFrame({'teamNo':team, 'posMost':'NA', 'shotsMost':0, 'accMost':0, 'posBest':'NA', 'shotsBest':0, 'accBest':0}, index=[0])
            df = pd.concat([df,nulldf], ignore_index=True)
    
    df = df.set_index('teamNo').sort_index().reset_index()
    return df
    
    
def favoritism(cycledf, teamlist):
    '''
    Parameters
    ----------
    cycledf : pd.DataFrame
        Contains cycle data from database and math columns for high goal makes and shots taken.
    teamlist: list of int
        list of all teams at the regional

    Returns
    -------
    teamprefdf: pd.DataFrame
        columns = ['teamNo', 'posMost', 'shotsMost', 'accMost', 'posBest', 'shotsBest', 'accBest']

    '''
    print('Starting favorites run')
    teamPosShots, posmap = maketeamshotsbypos(cycledf)
    
    teamfavs = findpos(teamPosShots, posmap, 'highShots')
    
    teambests = findpos(teamPosShots, posmap, 'accuracy')

    combodf = joinfavandbest(teamfavs, teambests)
    
    result = addmissingteams(combodf, teamlist)
   
    print(result)
    return result

def getFirstDayReportExcel(mainDf, cycleDf, pitDf):   
    #cycleDf = mainDf[1]
    #pitDf = readPitScout()
    mainData = mainDf
    cycleDf['highGoalMakes'] = cycleDf['outerGoalMakes'] + cycleDf['innerGoalMakes']
    cycleDf['highGoalShots'] = cycleDf['highGoalMakes'] + cycleDf['highGoalMisses']
    favortieSpotDf = favoritism(cycleDf,  getTeamList(mainData))
    cookedDf = getPrematchReportDf(mainDf, cycleDf, pitDf)
    mainData['climbCounter'] = 1
    climbData = mainData.set_index('teamNo').loc[:, ['climbLevel', 'climbCounter']]
    climbData = pd.pivot_table(climbData.reset_index(), index=['teamNo', 'climbLevel'], aggfunc=sum)
    climbSums = pd.pivot_table(climbData.reset_index(), index='teamNo', columns= 'climbLevel', aggfunc=sum, margins=True)
    climbSums.fillna(0, inplace=True)
    climbSums.drop('All', inplace=True)
    outfile = '1st Day report.xlsx'
    firstDayReport = pd.merge(cookedDf, climbSums, on='teamNo')
    firstDayReport = pd.merge(firstDayReport, favortieSpotDf, on='teamNo')
#    firstDayReport['Willing to Play Defense'] = pitDf['Are they willing to play defense if requested?']
#    firstDayReport['Anti-defensive capabilites'] = pitDf['Do they have anti-defense capabilities( a parking brake, shooting from a protected zone or wall, etc.)']
#    pprint(firstDayReport)
    with pd.ExcelWriter(outfile) as writer:
        mainDf = mainDf.sort_values(by = 'teamNo')   
        tabname = 'Raw Main Data'
        mainDf.to_excel(writer, tabname, index=False)
        cycleDf = cycleDf.sort_values(by = 'teamNo')
        tabname = 'Raw Cycle Data'
        cycleDf.to_excel(writer, tabname, index=False)
#        pitDf = pitDf.sort_values(by = 'Team number of the team you are scouting(not 1939 unless you are scouting us)')
        tabname = 'Raw Pit Data'
        pitDf.to_excel(writer, tabname, index=False)
        firstDayReport = firstDayReport.sort_values(by = 'teamNo')
        tabname = 'Analyzed Data'
        firstDayReport.to_excel(writer, tabname, index=False)
#    print('Day1Report written to file')
    
    


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


def getThatExcel(df, filename):
    today = datetime.today().strftime('%Y-%m-%d-%H-%M-%S')
    df.to_excel((str(filename) + str(today) + '.xlsx'))


def getTeamReport(prematchDf, mainDf, cycleDf, team, filepath, todir):
#    today = datetime.today().strftime('%Y-%m-%d-%H-%M-%S')
    prematchGraphs(mainDf, cycleDf, team)
    filename = str(team) + ' Team Report.html'
    with open(filename, 'w') as File:
        
        File.write('<html>')
        File.write('<head>')
        File.write('<meta name="viewport" content="width=device-width, initial-scale=1">')
        File.write('<style>')
        File.write('body {')
        File.write('font-family: Arial;')
        File.write('}')
        File.write('/* Style the tab */')
        File.write('.tab {')
        File.write('overflow: hidden;')
        File.write('border: 1px solid #ccc;')
        File.write('background-color: #f1f1f1;')
        File.write('}')
        File.write('/* Style the buttons inside the tab */')
        File.write('.tab button {')
        File.write('background-color: inherit;')
        File.write('float: left;')
        File.write('border: none;')
        File.write('outline: none;')
        File.write('cursor: pointer;')
        File.write('padding: 14px 16px;')
        File.write('transition: 0.3s;')
        File.write('font-size: 17px;')
        File.write('}')
        File.write('/* Change background color of buttons on hover */')
        File.write('.tab button:hover {')
        File.write('background-color: #ddd;')
        File.write('}')
        File.write('/* Create an active/current tablink class */')
        File.write('.tab button.active {')
        File.write('background-color: #ccc;')
        File.write('}')
        File.write('/* Style the tab content */')
        File.write('.tabcontent {')
        File.write('display: none;')
        File.write('padding: 6px 12px;')
        File.write('border: 1px solid #ccc;')
        File.write('border-top: none;')
        File.write('}')
        File.write('.graphSheet{')
        File.write('	width: 894px;')
        File.write('	display: inline-block;')
        File.write('	vertical-align:top')
        File.write('}')
        File.write('.team-card {')
        File.write('width: 400px;')
        File.write('display: inline-block;')
        File.write('}')
        File.write('.team-card-text {')
        File.write('padding: 0 40px;')
        File.write('}')
        File.write('</style>')
        File.write('</head>')
        File.write('<body>')
        File.write('<h2>Team Report</h2>')
        File.write('<h3>1939</h3>')
        File.write('<div class="team-card">')
        File.write('<div class="team-card">')
        File.write('      <img src=\"' + os.path.join(filepath, str(team) + '.jpg') + '\" alt="pic not found for team ' + str(team) + '" style="width:350px;height:400px;">')
        File.write('      <p>Team:' + str(team) + '</p>')
        File.write('      <p>Matches Scouted: ' + str(prematchDf.at[team, 'Matches Scouted'])+ ' </p>')
        File.write('      <p>Average Powercells Scored: '+ str(prematchDf.at[team, 'Average Pieces Scored']) + '</p>')
        File.write('      <p>Avg High Powercells Scored: ' + str(prematchDf.at[team, 'Average High Goal Makes'])+'</p>')
        File.write('	  <p>Tall or Short Bot: ' + str(prematchDf.at[team, 'bot height']) + '</p>')
        File.write('	  <p>Drivetrain: ' + str(prematchDf.at[team, 'drivetrain']) + '</p>')
        File.write('	  <p>Times Completed Rotational Control: ' + str(prematchDf.at[team, 'Times Completed Rotation Control' ]) + '</p>')
        File.write('	  <p>Times Completed Positional Control: ' + str(prematchDf.at[team,'Times Completed Positional Control' ]) + '</p>')
        File.write('	  <p>Matches Played on Defense: ' + str(prematchDf.at[team, 'Matches Played on Defense']) +   '</p>')
        File.write(mainDf.reset_index().set_index('teamNo').loc[[team], ['climbLevel']].to_html(index=False))
        File.write(mainDf.reset_index().set_index('teamNo').loc[[team], ['comments']].to_html(index=False))
        File.write('</div>')

        File.write('<div class="graphSheet">')
        File.write('	<img src="./' + str(team) + ' Prematch Graphs.png" alt="graph" style="width:894px">')
        File.write('</div>')
        File.write('</body>')
        File.write('</html>')              
        
        shutil.copy(str(team) + ' Team Report.html', todir)
        
        
        try: shutil.copy(os.path.join(filepath, str(team) + '.jpg'), todir)
        except: print('Photo not Found for ' + str(team))
        try: shutil.copy(str(team) + ' Prematch Graphs.png', todir)
        except: print('photo not found for ' + str(team))


    
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
    ax.figure.set_size_inches(len(teamList), 10)
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

def initPicklistGraph(teamList):
   fig = plt.figure(tight_layout=True, figsize=((len(teamList)+2), 10))
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
#    print(firstmove)
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
    for match in mainDf.reset_index().set_index('teamNo').loc[[team], ["matchNo"]].values:
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
#    plt.show()
   
    
def Main(testmode):
    print('press 1 to acquire a match list')
    print('press 2 to get a prematch scouting report')
    print('press 3 to get the day 1 report')
    print('press 4 to get a single team report')
    selection = input('enter number: ')
    selection = selection.lower()
    if selection == '1':
        event = input('enter event code: ')
        makeMatchList(event)
        
    elif selection == '2':
        # Team = enterTeam()       
        MainData, CycleData = readScout()
        MatchReport(FindPartners(readMatchList()), CycleData, MainData, 1939)


    elif selection == '3':
        mainDf, cycleDf = readScout()
        pitDf = readPitScout()
#        getPrematchReportDf
        getFirstDayReportExcel(mainDf, cycleDf, pitDf)
        picklistGraphs(mainDf, cycleDf)
        
    elif selection == '4':
        mainDf, cycleDf = readScout()
        pitDf = readPitScout()
 #       team = int(enterTeam())
        preMatchReport = getPrematchReportDf(mainDf, cycleDf, pitDf)
        filepath = filedialog.askdirectory(title='select directory from team photos')
        todir = filedialog.askdirectory(title='select directory to send the files')
        team = int(input('Enter Team Number: '))
        while team != 0:
            getTeamReport(preMatchReport, mainDf.reset_index(), cycleDf.reset_index(), team, filepath, todir)
            team = int(input('Enter team number or enter 0 to quit: '))

Main(True)
#mainDf, cycleDf = readScout()
