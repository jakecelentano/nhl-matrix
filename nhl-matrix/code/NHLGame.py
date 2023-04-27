import requests
from config import OBSERVE_DAYLIGHT_SAVINGS, STANDARD_TIMEZONE, DST_TIMEZONE
import datetime
import time
from game import Game

class NHLGame(Game):
    def __init__(self, id, link):
        super().__init__(id)
        self.id = id
        self.link = "https://statsapi.web.nhl.com" + link
        self.json = self.getJson() 
        self.timezone = self.getTimezone()

    # example in nhl_samples/game.json
    def getJson(self):
        return self.getData(self.link)  

    # ex: 2022020917
    def getId(self):
        return self.id

    # ex: https://statsapi.web.nhl.com/api/v1/game/2022020917/feed/live
    def getLink(self):
        return self.link
    
    
    def is_live(self):
        return self.getStatus().upper() == "LIVE"
    

    def getHomeScore(self):
        home_score = self.json['liveData']['boxscore']['teams']['home']['teamStats']['teamSkaterStats']['goals']
        return home_score
    
    def getAwayScore(self):
        away_score = self.json['liveData']['boxscore']['teams']['away']['teamStats']['teamSkaterStats']['goals']
        return away_score
    
    def getPeriod(self):
        return self.json['liveData']['linescore']['currentPeriod']
    
    def getPeriodTime(self):
        return self.json['liveData']['linescore']['currentPeriodTimeRemaining']


    # YYYY-MM-DD HH:MM:SS as datetime object
    def getDatetime(self):
        dt = datetime.datetime.strptime(self.json['gameData']['datetime']['dateTime'], "%Y-%m-%dT%H:%M:%SZ")
        self.time_zone = self.getTimezone()
        if self.time_zone == "UTC":
            return dt
        elif self.time_zone == "EST":
            return dt - datetime.timedelta(hours=5)
        elif self.time_zone == "EDT":
            return dt - datetime.timedelta(hours=4)
        elif self.time_zone == "CST":
            return dt - datetime.timedelta(hours=6)
        elif self.time_zone == "MST":
            return dt - datetime.timedelta(hours=7)
        elif self.time_zone == "PST":
            return dt - datetime.timedelta(hours=8)
        else:
            return dt
        
    def getSecondsUntilNextGame(self):
        return (self.getDatetime() - datetime.datetime.now()).total_seconds()

    # everything else is as a string, for convenience   
    # ex: 2019-10-21 19:00:00
    def getDatetimeString(self):
        return self.getDatetime().strftime("%Y-%m-%d %H:%M:%S")
    
    # ex: 2019-10-21
    def getDate(self):
        return self.getDatetimeString().split(" ")[0]
    
    # ex: 19:00:00
    def getTime(self):
        return self.getDatetimeString().split(" ")[1]
    
    # ex: 21
    def getDay(self):
        date  = str(self.getDate())
        return date.split("-")[2]
    
    # ex: 10
    def getMonth(self):
        date  = str(self.getDate())
        return date.split("-")[1]
    
    # ex: 2019
    def getYear(self):
        date  = str(self.getDate())
        return date.split("-")[0]

    # ex: Monday
    def getDayOfWeek(self):
        date  = str(self.getDate())
        return datetime.datetime.strptime(date, "%Y-%m-%d").strftime("%A")

    # ex: 07:00 PM
    def getTimePretty(self):
        time = str(self.getTime())
        hour = time.split(":")[0]
        minute = time.split(":")[1]
        if int(hour) > 12:
            hour = int(hour) - 12
            return "{}:{} PM".format(hour, minute)
        else:
            return "{}:{} AM".format(hour, minute)

    def getStatus(self):
        try:
            status = self.json['gameData']['status']['abstractGameState']
        except:
            status = "NULL"
            print("Error getting game status")
            print(self.json)
        return status

    def getTeams(self):
        return self.json['teams']

    def getHomeTeamId(self):
        return self.json['gameData']['teams']['home']['id']

    def getAwayTeamId(self):
        return self.json['gameData']['teams']['away']['id']

    def getHomeTeamName(self):
        return self.json['gameData']['teams']['home']['name']
    
    def getAwayTeamName(self):
        return self.json['gameData']['teams']['away']['name']

    def prettyPrint(self):
        print("{} vs {} - {} @ {}".format(self.get_game_home_team_name(), self.get_game_away_team_name(), self.get_game_date_prety(), self.get_game_time_prety()))

    def prettyPrintString(self):
        return "{} vs {} - {} @ {}".format(self.get_game_home_team_name(), self.get_game_away_team_name(), self.get_game_date_prety(), self.get_game_time_prety())

    def getTimezone(self):
        if OBSERVE_DAYLIGHT_SAVINGS:
            if time.daylight:
                return DST_TIMEZONE
            else:
                return STANDARD_TIMEZONE
        else:
            return STANDARD_TIMEZONE
        



