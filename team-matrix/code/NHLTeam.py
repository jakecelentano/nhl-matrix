import requests
from NHLPlayer import NHLPlayer
from NHLGame import NHLGame
from team import Team
import datetime
import cairosvg
import os
import json
import time

class NHLTeam(Team):
    def __init__(self, id, name, abbreviation, link, league="NHL"):
        super().__init__(id, name, abbreviation, link, league)
        self.id = id
        self.name = name
        self.abbreviation = abbreviation
        self.link = link
        self.league = league
        self.players = []
        self.json = None
        self.stats = None

    
    def getJson(self):
        self.json = self.getData('https://statsapi.web.nhl.com/api/v1/teams/{}'.format(self.id))
        return self.json

    def getRoster(self):
        roster = []
        json = self.getData(self.team_link + '/roster')
        for player in json['roster']:
            roster.append(NHLPlayer(player['person']['id'], player['person']['fullName'], player['person']['link']))
        return roster
    
    def getSchedule(self, start_date, end_date):
        games = []
        json = self.getData('https://statsapi.web.nhl.com/api/v1/schedule?startDate={}&endDate={}&teamId={}'.format(start_date, end_date, self.id))

        for date in json['dates']:
            for game in date['games']:
                games.append(NHLGame(game['gamePk'], game['link']))
        return games

    def getNextGames(self, num_games=2):
        # searches 2 weeks at a time until it finds enough games
        days = 14
        start_date = datetime.datetime.now().strftime("%Y-%m-%d")
        end_date = (datetime.datetime.now() + datetime.timedelta(days=days)).strftime("%Y-%m-%d")
        games = self.getSchedule(start_date, end_date)
        num = len(games)
        while num < num_games:
            days += 14
            end_date = (datetime.datetime.now() + datetime.timedelta(days=days)).strftime("%Y-%m-%d")
            games = self.getSchedule(start_date, end_date)
            num = len(games)
        return games[:num_games]
    

    def getLogo(self):
        NHL_LOGO_API_PREFIX = "https://www-league.nhlstatic.com/images/logos/teams-current-primary-light"
        if os.path.isfile('logos/{}.png'.format(self.name)):
            return 'logos/{}.png'.format(self.name)
        else:
            url = NHL_LOGO_API_PREFIX + '/{}.svg'.format(self.id)
            try:
                cairosvg.svg2png(url=url, write_to='logos/{}.png'.format(self.name), output_width=100, output_height=100)
            except:
                print("Couldn't get logo for {}".format(self.name))
                print(url)
                print("Using default logo")
                return 'logos/{}.png'.format('nhl')          
        return 'logos/{}.png'.format(self.name)
    
    def getStats(self):
        self.stats = self.getData('https://statsapi.web.nhl.com/api/v1/teams/{}/stats'.format(self.id))
        return self.stats
    
    def getWins(self):
        if self.stats is None:
            self.getStats()
        return self.stats['stats'][0]['splits'][0]['stat']['wins']
    
    def getLosses(self):
        if self.stats is None:
            self.getStats()
        return self.stats['stats'][0]['splits'][0]['stat']['losses']

    def getOT(self):
        if self.stats is None:
            self.getStats()
        return self.stats['stats'][0]['splits'][0]['stat']['ot']
    
    def getColors(self):
        path = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(path, 'colors//nhl_colors.json')
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