import requests
from NHLTeam import NHLTeam
from NHLGame import NHLGame
import json


class NHL(object):
    def __init__(self):
        self.teams = self.get_teams()

    def get_teams(self):
        teams = []
        teams_json = requests.get('https://statsapi.web.nhl.com/api/v1/teams').json()
        for team in teams_json['teams']:
            teams.append(NHLTeam(team['id'], team['name'], team['abbreviation'], team['link']))
        return teams

    def get_team_by_name(self, name):
        for team in self.teams:
            if team.team_name == name:
                return team

    def get_team_by_id(self, team_id):
        for team in self.teams:
            if team.team_id == team_id:
                return team

    def get_schedule(self, start_date, end_date):
        games = []
        schedule_json = requests.get('https://statsapi.web.nhl.com/api/v1/schedule?startDate={}&endDate={}'.format(start_date, end_date)).json()

        for date in schedule_json['dates']:
            for game in date['games']:
                games.append(NHLGame(game['gamePk'], game['link']))
        return games
    
