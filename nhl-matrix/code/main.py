#!/usr/bin/env python
# Display a runtext with double-buffering.
from samplebase import SampleBase
from rgbmatrix import graphics
import time
from nhl import NHL
from team import Team
from PIL import Image
import datetime
from config import TEAMS
from nhlscreen import NHLScreen

BRUINS_YELLOW = graphics.Color(253, 185, 39)
BRUINS_BLACK = graphics.Color(0, 0, 0)

class GamesTracker(SampleBase):
    def __init__(self, *args, **kwargs):
        super(GamesTracker, self).__init__(*args, **kwargs)
        self.parser.add_argument("-t", "--text", help="The text to scroll on the RGB LED panel", default="Hello world!")
        self.nhl = NHL(str(datetime.datetime.now().year))

    def run(self):
        year = datetime.datetime.now().year
        nhl = NHL(year)
<<<<<<< HEAD
        screen = NHLScreen()
=======
        bruins = nhl.get_team_by_name("Boston Bruins")
        games = bruins.get_next_games(2)
        game = games[0]
        hid = game.get_game_home_team_id()
        aid = game.get_game_away_team_id()
        print(hid)
        print(aid)
        home_team = self.nhl.get_team_by_id(hid)
        away_team = self.nhl.get_team_by_id(aid)
        home_team_logo = home_team.get_logo()
        away_team_logo = away_team.get_logo()
        print(home_team_logo)
        print(away_team_logo)
        return

        self.drawUpcomingGamesScreen(offscreen_canvas, games)
        self.drawBorder(offscreen_canvas)
        time.sleep(100)
        
        #next_games = bruins.get_next_games(2)
        #next_game = next_games[0]
        #my_text = next_game.pretty_print_string()

        #while True:
        #    offscreen_canvas.Clear()
        #    len = graphics.DrawText(offscreen_canvas, font, pos, 10, textColor, my_text)
        #    pos -= 1
        #    if (pos + len < 0):
        #        pos = offscreen_canvas.width

        #    time.sleep(0.05)
        #    offscreen_canvas = self.matrix.SwapOnVSync(offscreen_canvas)
    
    def drawUpcomingGamesScreen(self, offscreen_canvas, games=[]):
        x = 2
        y = 2
        for game in games:
            home_team = self.nhl.get_team_by_id(game.get_game_home_team_id())
            away_team = self.nhl.get_team_by_id(game.get_game_away_team_id())
            home_team_logo = home_team.get_logo()
            away_team_logo = away_team.get_logo()
            home_team_logo = Image.open(home_team_logo)
            away_team_logo = Image.open(away_team_logo)
            home_team_logo.thumbnail((30, 30), Image.ANTIALIAS)
            away_team_logo.thumbnail((30, 30), Image.ANTIALIAS)
            home_team_logo = home_team_logo.convert('RGB')
            away_team_logo = away_team_logo.convert('RGB')
            offscreen_canvas.SetImage(home_team_logo, x, y)
            offscreen_canvas.SetImage(away_team_logo, x+30, y)
            y += 30
        offscreen_canvas = self.matrix.SwapOnVSync(offscreen_canvas)

    def drawBorder(self, offscreen_canvas):
        graphics.DrawLine(offscreen_canvas, 0, 0, 63, 0, BRUINS_YELLOW)
        graphics.DrawLine(offscreen_canvas, 0, 0, 0, 63, BRUINS_YELLOW)
        graphics.DrawLine(offscreen_canvas, 63, 0, 63, 63, BRUINS_YELLOW)
        graphics.DrawLine(offscreen_canvas, 0, 63, 63, 63, BRUINS_YELLOW)
        offscreen_canvas = self.matrix.SwapOnVSync(offscreen_canvas)
>>>>>>> 67a16a709b0c072aa7608c1570916eff79d0c61e

        while True:
            for team in TEAMS:
                team = nhl.get_team_by_name(team)
                screen.drawUpcomingGamesScreen(team)
                time.sleep(10)
            

# Main function
if __name__ == "__main__":
    games_tracker = GamesTracker()
    if (not games_tracker.process()):
        print("Error processing arguments")
        games_tracker.print_help()
