import requests
import time
from config import DEFAULT_HEADERS, SHOW_REQUESTS

class Game:
    def __init__(self, id):
        self.id = id
        self.headers =  DEFAULT_HEADERS

    def getId(self):
        return self.id
    
    def getData(self, url):
        retries = 0
        json = None
        while retries < 1 and not json:
            try:
                if SHOW_REQUESTS:
                    print(url)
                json = requests.get(url, headers=self.headers).json()
            except:
                retries += 1
                time.sleep(10)
        
        if not json:
            raise Exception("Couldn't get data from {}".format(url))
        
        return json
        