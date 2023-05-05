import requests
from nba_api.stats.static import teams
from NBATeam import NBATeam
from league import League
import json


class NBA(League):
    def __init__(self, name="NBA"):
        super().__init__(name, "Basketball")
        self.teams = self.getTeams()
    
    def getTeams(self):
        teams_list = []
        nba_teams = teams.get_teams()
        for team in nba_teams:
            teams_list.append(NBATeam(team['id'], team['full_name'], team['abbreviation']))
        return teams_list
        
    
    def getTeam(self, search):
        search = search.lower()
        for team in self.teams:
            if search in team.name.lower():
                return team
            if search in team.abbreviation.lower():
                return team
            if search == team.id:
                return team
    
    def getSchedule(self, start_date, end_date):
        pass

