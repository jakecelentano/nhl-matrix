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
from samplebase import SampleBase


def main():
    nhl = NHL(str(datetime.datetime.now().year))
    screen = NHLScreen()

    while True:
        for team in TEAMS:
            team = nhl.get_team_by_name(team)
            screen.drawUpcomingGamesScreen(team)
            time.sleep(10)

if __name__ == "__main__":
    main()