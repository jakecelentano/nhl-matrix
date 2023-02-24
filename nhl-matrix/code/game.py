import requests
from config import STATS_API_PREFIX, OBSERVE_DAYLIGHT_SAVINGS, STANDARD_TIMEZONE, DST_TIMEZONE
import datetime

class Game(object):
    def __init__(self, game_id, game_link):
        self.game_id = game_id
        self.game_link = STATS_API_PREFIX + game_link
        self.game_json = self.get_game_json() 
        self.time_zone = self.get_time_zone() 

    def get_game_json(self):
        result = ""
        try:
            result = requests.get(self.game_link).json()
        except:
            print("Error")
        return result

    def get_game_id(self):
        return self.game_id

    def get_game_link(self):
        return self.game_link

    # YYYY-MM-DD HH:MM:SS
    def get_game_datetime(self):
        dt = datetime.datetime.strptime(self.game_json['gameData']['datetime']['dateTime'], "%Y-%m-%dT%H:%M:%SZ")
        if self.time_zone == "UTC":
            return dt
        elif self.time_zone == "EST":
            return dt + datetime.timedelta(hours=5)
        elif self.time_zone == "EDT":
            return dt + datetime.timedelta(hours=4)
        elif self.time_zone == "CST":
            return dt + datetime.timedelta(hours=6)
        elif self.time_zone == "MST":
            return dt + datetime.timedelta(hours=7)
        elif self.time_zone == "PST":
            return dt + datetime.timedelta(hours=8)
        else:
            return dt

    def get_game_datetime_string(self):
        return self.get_game_datetime().strftime("%Y-%m-%d %H:%M:%S")
    
    def get_game_date(self):
        return self.get_game_datetime_string().split(" ")[0]

    def get_game_date_prety(self):
        date  = str(self.get_game_date())
        year = date.split("-")[0]
        month = date.split("-")[1]
        day = date.split("-")[2]
        day_of_week = datetime.datetime.strptime(date, "%Y-%m-%d").strftime("%A")
        return "{} {}/{}/{}".format(day_of_week, month, day, year)
    
    def get_game_time_prety(self):
        time = str(self.get_game_time())
        hour = time.split(":")[0]
        minute = time.split(":")[1]
        if int(hour) > 12:
            hour = int(hour) - 12
            return "{}:{} PM".format(hour, minute) + " " + self.time_zone
        else:
            return "{}:{} AM".format(hour, minute) + " " + self.time_zone




    def get_game_time(self):
        return self.get_game_datetime_string().split(" ")[1]


    def get_game_status(self):
        return self.game_json['status']['abstractGameState']

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
            if datetime.datetime.now().dst():
                return DST_TIMEZONE
            else:
                return STANDARD_TIMEZONE
        else:
            return STANDARD_TIMEZONE

