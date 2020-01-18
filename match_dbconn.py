import mysql.connector as mariadb

#mariadb_connection = mariadb.connect(user='mscout',password='mscout',host='localhost',database='match_scout')
mariadb_connection = mariadb.connect(user='mscout',password='mscout',host='192.168.100.31',database='match_scout')
cursor = mariadb_connection.cursor()


def getMatchNo(team_no):
   # print(team_no)
    sql = "select matchNo from matchInfo where teamNo = %s"  
    cursor.execute(sql,(team_no,))
    row = cursor.fetchone()
    return row[0]

def getMatchInfo(match_no,pos):
   # print(match_no,pos)
    sql = "select teamNo from matchInfo where matchNo = %s and position = %s"
    cursor.execute(sql,(match_no,pos,))
    row = cursor.fetchone()
    return row[0]

def getAllMatchInfo(match_no,pos):
   # print("Match No = ",match_no)
   
    sql = "select teamNo,scoutName from matchInfo where matchNo = %s and position = %s"
    cursor.execute(sql,(match_no,pos,))
    row = cursor.fetchone()
    return row

def getNextMatch():
    sql = "select matchNo from matchCurrent where id = 1"
    cursor.execute(sql)
    row = cursor.fetchone()
 #   print('from get_next_match %s',row[0])
    return row[0]

def checkScoutData(match,team):
    result = 0
    sql = "select  id from matchScout where matchNo = %s and teamNo = %s"
    cursor.execute(sql,(match,team,))
    row = cursor.fetchone()
    count = cursor.rowcount
    print("Count = ",count)
    if count > 0:
        result = 1
    return result

def setCurrentMatch(currentMatch):
  #  print("Calling with ",currentMatch)
    sql = "update matchCurrent set matchNo = %s where id = 1"
    cursor.execute(sql,(currentMatch,))
    mariadb_connection.commit()

def setScout(scoutName,currentMatch,pos):
 #   print("Calling with ",currentMatch,pos)
    sql = "update matchInfo set scoutName = %s where matchNo = %s and position = %s"
    cursor.execute(sql,(scoutName,currentMatch,pos,))
    mariadb_connection.commit()

def setAllMatchInfo(matchNo,teamNo,pos):
    sql = "insert into matchInfo (matchNo,teamNo,position) values(%s,%s,%s)"
    cursor.execute(sql,(matchNo,teamNo,pos,))
    mariadb_connection.commit()

def clearMatchInfo():
    sql = "truncate table matchInfo"
    cursor.execute(sql)

def clearMatchScout(matchNo):
    sql = "delete from matchScout where matchNo = %s"
    cursor.execute(sql,(matchNo,))
    mariadb_connection.commit()

def setMatchCycle(matchNo,
                  teamNo,
                  shooterPositionTeleop,
                  lowGoalMissesTele,
                  highGoalMissesTele,
                  lowGoalMakesTele,
                  outerGoalMakesTele,
                  innerGoalMakesTele,
                  gameTime):
    sql = "insert into matchCycle ( matchNo, \
                                    teamNo, \
                                    shooterPositionTeleop, \
                                    lowGoalMissesTele, \
                                    highGoalMissesTele, \
                                    lowGoalMakesTele, \
                                    outerGoalMakesTele, \
                                    innerGoalMakesTele, \
                                    gameTime) \
            values(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    cursor.execute(sql,(matchNo,
                        teamNo,
                        shooterPositionTeleop,
                        lowGoalMissesTele,
                        highGoalMissesTele,
                        lowGoalMakesTele,
                        outerGoalMakesTele,
                        innerGoalMakesTele,
                        gameTime))
     mariadb_connection.commit()   
                        

def setMatchScout(matchNo,
                  teamNo,
                  scoutName,
                  scoutTeamNo,
                  startPos,
                  crossInitiationLine,
                  shotterPositionAuto,
                  lowGoalMissesAuto,
                  highGoalMissesAuto,
                  lowGoalMakesAuto,
                  highGoalMakesAuto,
                  outerGoalMakesAuto,
                  innerGoalMakesAuto,
                  ballsPickedUpAuto,
                  foulsAuto,
                  techFoulsAuto,
                  shooterPositionTele,
                  lowGoalMissesTele,
                  highGoalMissesTele,
                  lowGoalMakesTele,
                  outerGoalMakesTele,
                  innterGoalMakesTele,
                  foulsTele,
                  techFoulsTele,
                  defense,
                  rotationControl,
                  positionalControl,
                  fellOffBar,
                  buddyClimb,
                  hitClimbingTeam,
                  leveledBar,
                  climbedFromBarOrRung,
                  climbLevel,
                  deadbot,
                  comments,
                  tippedOver,
                  recoveredFromDead,
                  cards):
    sql = "insert into matchScout (matchNo, \
                  teamNo, \
                  scoutName, \
                  scoutTeamNo, \
                  startPos, \
                  crossInitiationLine, \
                  shotterPositionAuto, \
                  lowGoalMissesAuto, \
                  highGoalMissesAuto, \
                  lowGoalMakesAuto, \
                  highGoalMakesAuto, \
                  outerGoalMakesAuto, \
                  innerGoalMakesAuto, \
                  ballsPickedUpAuto, \
                  foulsAuto, \
                  techFoulsAuto, \
                  shooterPositionTele, \
                  lowGoalMissesTele, \
                  highGoalMissesTele, \
                  lowGoalMakesTele, \
                  outerGoalMakesTele, \
                  innterGoalMakesTele, \
                  foulsTele, \
                  techFoulsTele, \
                  defense, \
                  rotationControl, \
                  positionalControl, \
                  fellOffBar, \
                  buddyClimb, \
                  hitClimbingTeam, \
                  leveledBar, \
                  climbedFromBarOrRung, \
                  climbLevel, \
                  deadbot, \
                  comments, \
                  tippedOver, \
                  recoveredFromDead, \
                  cards) \
    values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s, \
           %s,%s,%s,%s,%s,%s,%s,%s,%s,%s, \
           %s,%s,%s,%s,%s,%s,%s,%s,%s,%s, \
           %s,%s,%s,%s,%s,%s,%s,%s)"
    cursor.execute(sql,(matchNo,
                  teamNo,
                  scoutName,
                  scoutTeamNo,
                  startPos,
                  crossInitiationLine,
                  shotterPositionAuto,
                  lowGoalMissesAuto,
                  highGoalMissesAuto,
                  lowGoalMakesAuto,
                  highGoalMakesAuto,
                  outerGoalMakesAuto,
                  innerGoalMakesAuto,
                  ballsPickedUpAuto,
                  foulsAuto,
                  techFoulsAuto,
                  shooterPositionTele,
                  lowGoalMissesTele,
                  highGoalMissesTele,
                  lowGoalMakesTele,
                  outerGoalMakesTele,
                  innterGoalMakesTele,
                  foulsTele,
                  techFoulsTele,
                  defense,
                  rotationControl,
                  positionalControl,
                  fellOffBar,
                  buddyClimb,
                  hitClimbingTeam,
                  leveledBar,
                  climbedFromBarOrRung,
                  climbLevel,
                  deadbot,
                  comments,
                  tippedOver,
                  recoveredFromDead,
                cards))   
    mariadb_connection.commit() 
                  
    





