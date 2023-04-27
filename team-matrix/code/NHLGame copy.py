import requests
from config import STATS_API_PREFIX, OBSERVE_DAYLIGHT_SAVINGS, STANDARD_TIMEZONE, DST_TIMEZONE, DEFAULT_HEADERS
import datetime
import time

class NHLGame(object):
    def __init__(self, id, link):
        self.id = id
        self.game_link = STATS_API_PREFIX + link
        self.game_json = self.get_game_json() 
        self.time_zone = self.get_time_zone()
        self.headers = DEFAULT_HEADERS

    # example in nhl_samples/game.json
    def get_game_json(self):
        result = ""
        retries = 0

        while not result and retries < 5:
            try:
                self.headers = DEFAULT_HEADERS
                result = requests.get(url=self.game_link, headers=self.headers).json()
            except:
                print("Error getting game json")
                retries += 1
                time.sleep(10)
           
        return result

    # ex: 2022020917
    def get_game_id(self):
        return self.game_id

    # ex: https://statsapi.web.nhl.com/api/v1/game/2022020917/feed/live
    def get_game_link(self):
        return self.game_link
    
    
    def is_live(self):
        return self.get_status().upper() == "LIVE"
    

    def get_home_score(self):
        home_score = self.game_json['liveData']['boxscore']['teams']['home']['teamStats']['teamSkaterStats']['goals']
        return home_score
    
    def get_away_score(self):
        away_score = self.game_json['liveData']['boxscore']['teams']['away']['teamStats']['teamSkaterStats']['goals']
        return away_score
    
    def get_period(self):
        return self.game_json['liveData']['linescore']['currentPeriod']
    
    def get_period_time(self):
        return self.game_json['liveData']['linescore']['currentPeriodTimeRemaining']


    # YYYY-MM-DD HH:MM:SS as datetime object
    def get_game_datetime(self):
        dt = datetime.datetime.strptime(self.game_json['gameData']['datetime']['dateTime'], "%Y-%m-%dT%H:%M:%SZ")
        self.time_zone = self.get_time_zone()
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
        
    def get_seconds_until_next_game(self):
        return (self.get_game_datetime() - datetime.datetime.now()).total_seconds()

    # everything else is as a string, for convenience   
    # ex: 2019-10-21 19:00:00
    def get_game_datetime_string(self):
        return self.get_game_datetime().strftime("%Y-%m-%d %H:%M:%S")
    
    # ex: 2019-10-21
    def get_game_date(self):
        return self.get_game_datetime_string().split(" ")[0]
    
    # ex: 19:00:00
    def get_game_time(self):
        return self.get_game_datetime_string().split(" ")[1]
    
    # ex: 21
    def get_game_day(self):
        date  = str(self.get_game_date())
        return date.split("-")[2]
    
    # ex: 10
    def get_game_month(self):
        date  = str(self.get_game_date())
        return date.split("-")[1]
    
    # ex: 2019
    def get_game_year(self):
        date  = str(self.get_game_date())
        return date.split("-")[0]

    # ex: Monday
    def get_game_day_of_week(self):
        date  = str(self.get_game_date())
        return datetime.datetime.strptime(date, "%Y-%m-%d").strftime("%A")

    # ex: Monday 10/21/2019
    def get_game_date_prety(self):
        date  = str(self.get_game_date())
        year = date.split("-")[0]
        month = date.split("-")[1]
        day = date.split("-")[2]
        day_of_week = datetime.datetime.strptime(date, "%Y-%m-%d").strftime("%A")
        return "{} {}/{}/{}".format(day_of_week, month, day, year)
    
    # ex: 07:00 PM
    def get_game_time_pretty(self):
        time = str(self.get_game_time())
        hour = time.split(":")[0]
        minute = time.split(":")[1]
        if int(hour) > 12:
            hour = int(hour) - 12
            return "{}:{} PM".format(hour, minute)
        else:
            return "{}:{} AM".format(hour, minute)






    def get_status(self):
        try:
            status = self.game_json['gameData']['status']['abstractGameState']
        except:
            status = "NULL"
            print("Error getting game status")
            print(self.game_json)
        return status

    def get_game_teams(self):
        return self.game_json['teams']

    def get_game_home_team_id(self):
        return self.game_json['gameData']['teams']['home']['id']

    def get_game_away_team_id(self):
        return self.game_json['gameData']['teams']['away']['id']

    def get_game_home_team_name(self):
        return self.game_json['gameData']['teams']['home']['name']
    
    def get_game_away_team_name(self):
        return self.game_json['gameData']['teams']['away']['name']

    def pretty_print(self):
        print("{} vs {} - {} @ {}".format(self.get_game_home_team_name(), self.get_game_away_team_name(), self.get_game_date_prety(), self.get_game_time_prety()))

    def pretty_print_string(self):
        return "{} vs {} - {} @ {}".format(self.get_game_home_team_name(), self.get_game_away_team_name(), self.get_game_date_prety(), self.get_game_time_prety())

    def get_time_zone(self):
        if OBSERVE_DAYLIGHT_SAVINGS:
            if time.daylight:
                return DST_TIMEZONE
            else:
                return STANDARD_TIMEZONE
        else:
            return STANDARD_TIMEZONE
        



