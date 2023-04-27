import requests


class Statistic(object):
    def __init__(self, stat_type, stat):
        self.stat_type = stat_type
        self.stat = stat

    def __str__(self):
        return self.stat_type

    def __repr__(self):
        return self.stat_type

    def get_stat_type(self):
        return self.stat_type

    def get_stat(self):
        return self.stat