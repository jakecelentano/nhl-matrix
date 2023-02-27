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

class RunText(SampleBase):
    def __init__(self, *args, **kwargs):
        super(RunText, self).__init__(*args, **kwargs)
        self.parser.add_argument("-t", "--text", help="The text to scroll on the RGB LED panel", default="Hello world!")
        self.nhl = NHL(str(datetime.datetime.now().year))

    def run(self):

        year = datetime.datetime.now().year
        nhl = NHL(year)
        screen = NHLScreen()
        for team in TEAMS:
            team = nhl.get_team_by_name(team)
            screen.drawUpcomingGamesScreen(team)
            time.sleep(10)
            




# Main function
if __name__ == "__main__":
    run_text = RunText()
    if (not run_text.process()):
        print("Error processing arguments")
        run_text.print_help()
