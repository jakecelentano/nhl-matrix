import requests
import time
from config import DEFAULT_HEADERS, SHOW_REQUESTS
class Team:
    def __init__(self, id, name, abbreviation, link, league):
        self.id = id
        self.name = name
        self.abbreviation = abbreviation
        self.link = link
        self.league = league
        self.players = []
        self.headers =  DEFAULT_HEADERS


    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name
    
    def getId(self):
        return self.id
            
    def getName(self):
        return self.name
    
    def getAbbreviation(self):
        return self.abbreviation
    
    def getLink(self):
        return self.link
    
    def getLeague(self):
        return self.league
    
    def getPlayers(self):
        return self.players
    
    def getPlayer(self, name):
        for player in self.players:
            if player.name == name:
                return player
            
    def getPlayerById(self, id):
        for player in self.players:
            if player.id == id:
                return player
    
    def getData(self, url):
        retries = 0
        json = None
        while retries < 10 and not json:
            try:
                if SHOW_REQUESTS:
                    print(url)
                json = requests.get(url, headers=self.headers).json()
            except:
                retries += 1
                time.sleep(retries)
        
        if not json:
            raise Exception("Couldn't get data from {}".format(url))
        
        return json
    
    def hexToRGB(self, hex):
        hex = hex.lstrip('#')
        hlen = len(hex)
        return tuple(int(hex[i:i+hlen//3], 16) for i in range(0, hlen, hlen//3))
    