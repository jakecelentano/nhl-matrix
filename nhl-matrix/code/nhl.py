import requests
from NHLTeam import NHLTeam
from NHLGame import NHLGame
from league import League
import json


class NHL(League):
    def __init__(self, name="NHL"):
        super().__init__(name, "Hockey")
        self.teams = self.getTeams()
    
    def getTeams(self):
        teams = []
        teams_json = self.getData('https://statsapi.web.nhl.com/api/v1/teams')
        for team in teams_json['teams']:
            teams.append(NHLTeam(team['id'], team['name'], team['abbreviation'], team['link']))
        return teams
    
    def getTeam(self, team):
        for team in self.teams:
            if team.team_id == team:
                return team
            if team.abbreviation == team:
                return team
            if team.name == team:
                return team   
        return None
    
    def getSchedule(self, start_date, end_date):
        games = []
        schedule_json = self.getData('https://statsapi.web.nhl.com/api/v1/schedule?startDate={}&endDate={}'.format(start_date, end_date))
        for date in schedule_json['dates']:
            for game in date['games']:
                games.append(NHLGame(game['gamePk'], game['link']))
        return games
    

