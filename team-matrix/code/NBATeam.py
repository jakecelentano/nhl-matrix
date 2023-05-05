import requests
from team import Team
import datetime
import cairosvg
import os
import json
import time
from nba_api.stats.static import teams
from nba_api.stats.endpoints import teamgamelog
from nba_api.stats.endpoints import commonplayerinfo
from nba_api.stats.endpoints import leaguegamefinder
from nba_api.stats.endpoints import teaminfocommon
from nba_api.stats.endpoints import teamyearbyyearstats
from nba_api.stats.endpoints import teamdashboardbyyearoveryear
from nba_api.stats.endpoints import teamdetails
from nba_api.stats.endpoints import teamplayerdashboard
from nba_api.stats.endpoints import teamdashlineups

class NBATeam(Team):
    def __init__(self, id, name, abbreviation, link=None, league="NBA"):
        super().__init__(id, name, abbreviation, link, league)
        self.id = id
        self.name = name
        self.abbreviation = abbreviation
        self.league = league
        self.players = []
        self.json = None
        self.stats = None

    
    def getJson(self):
        if self.json == None:
            self.json = self.getTeamJson()
        return self.json

    def getRoster(self):
        pass
    
    def getSchedule(self, start_date, end_date):
        # get schedule for team between start_date and end_date
        season = start_date.year
        season = str(season) + '-' + str(season + 1)[2:]
        game_log = teamgamelog.TeamGameLog(self.id, season=season, season_type_all_star='Playoffs')
        game_log = game_log.get_data_frames()[0]
        game_log = game_log[(game_log['GAME_DATE'] >= start_date.strftime('%Y-%m-%d')) & (game_log['GAME_DATE'] <= end_date.strftime('%Y-%m-%d'))]
        return game_log


    def getNextGames(self, num_games=1):
        pass
    
    def getPreviousGames(self, num_games=1):
        pass
    

    def getLogo(self):
        pass      
        
    
    def getStats(self):
        pass
    
    def getWins(self):
        pass
    
    def getLosses(self):
        pass


    def getOT(self):
        pass
    
    def getColors(self):
        path = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(path, 'colors//nba_colors.json')
        file = open(file_path, 'r')
        data = json.load(file)
        
        for team in data:
            if team['name'] == self.name:
                colors = team['colors']['hex']
                colors = [self.hexToRGB(color) for color in colors]
                return colors    
        return [self.hexToRGB('#123456'), self.hexToRGB('#FFFFFF')]
    
    def getPrimaryColor(self):
        colors = self.getColors()
        for color in colors:
            r = color[0]
            g = color[1]
            b = color[2]
            luma = 0.2126 * r + 0.7152 * g + 0.0722 * b
            if (luma > 40):
                return color          
        return (255, 255, 255)