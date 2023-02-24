import requests
from statistic import Statistic
from config import STATS_API_PREFIX

class Player(object):
    def __init__(self, player_id, player_name, player_link):
        self.player_id = player_id
        self.player_name = player_name
        self.player_link = STATS_API_PREFIX + player_link

    def __str__(self):
        return self.player_name

    def __repr__(self):
        return self.player_name

    def get_player_id(self):
        return self.player_id

    def get_stats(self):
        stats = []
        stats_json = requests.get(self.player_link + '/stats').json()
        return None
        for stat in stats_json['stats'][0]['splits']:
            stats.append(Statistic(stat['stat']))
        return stats