import requests
from player import Player
from game import Game
from setup import STATS_API_PREFIX
import datetime

class Team(object):
    def __init__(self, team_id, team_name, team_abbreviation, team_link):
        self.team_id = team_id
        self.team_name = team_name
        self.team_abbreviation = team_abbreviation
        self.team_link = STATS_API_PREFIX + team_link

    def __str__(self):
        return self.team_name

    def __repr__(self):
        return self.team_name

    def get_team_id(self):
        return self.team_id


    def get_roster(self):
        roster = []
        roster_json = requests.get(self.team_link + '/roster').json()
        for player in roster_json['roster']:
            roster.append(Player(player['person']['id'], player['person']['fullName'], player['person']['link']))
        return roster

    def player_by_name(self, name):
        for player in self.get_roster():
            if player.player_name == name:
                return player

    def get_schedule(self, start_date, end_date):
        games = []
        schedule_json = requests.get('https://statsapi.web.nhl.com/api/v1/schedule?startDate={}&endDate={}&teamId={}'.format(start_date, end_date, self.team_id)).json()
        for date in schedule_json['dates']:
            for game in date['games']:
                games.append(Game(game['gamePk'], game['link']))
        return games

    def get_next_games(self, num_games):
        days = 14
        start_date = datetime.datetime.now().strftime("%Y-%m-%d")
        end_date = (datetime.datetime.now() + datetime.timedelta(days=days)).strftime("%Y-%m-%d")
        games = self.get_schedule(start_date, end_date)
        num = len(games)
        while num < num_games:
            days += 14
            end_date = (datetime.datetime.now() + datetime.timedelta(days=days)).strftime("%Y-%m-%d")
            games = self.get_schedule(start_date, end_date)
            num = len(games)
        return games[:num_games]


        
