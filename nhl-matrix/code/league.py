import requests
import time

class League:
    def __init__(self, name, sport):
        self.name = name
        self.sport = sport
        self.teams = []


    def getTeams(self):
        return self.teams
    
    # get team by name or abbreviation
    def getTeam(self, name):
        for team in self.teams:
            if team.name == name:
                return team
        for team in self.teams:
            if team.abbreviation == name:
                return team
        return None
            
    def getTeamById(self, id):
        for team in self.teams:
            if team.id == id:
                return team
            
    def getData(self, url):
        retries = 0
        json = None
        while retries < 10 and not json:
            try:
                json = requests.get(url).json()
            except:
                retries += 1
                time.sleep(10)
        
        if not json:
            raise Exception("Couldn't get data from {}".format(url))
        
        return json