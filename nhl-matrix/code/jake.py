#!/usr/bin/env python
from samplebase import SampleBase
from rgbmatrix import graphics
import time
from nhl import NHL
from team import Team
import datetime
from config import DEFAULT_TEAM



class Jake(SampleBase):
    def __init__(self, *args, **kwargs):
        super(Jake, self).__init__(*args, **kwargs)

    def run(self):
        offscreen_canvas = self.matrix.CreateFrameCanvas()
        nhl = NHL(str(datetime.datetime.now().year))
        team = nhl.get_team_by_name(DEFAULT_TEAM)
        team_primary_color = team.get_primary_color()
        color = graphics.Color(team_primary_color[0], team_primary_color[1], team_primary_color[2])
        while True:
            self.drawBorder(color)
            time.sleep(5)

    
    def drawBorder(self, color):
        offscreen_canvas = self.matrix.CreateFrameCanvas()
        graphics.DrawLine(offscreen_canvas, 0, 0, 63, 0, color)
        graphics.DrawLine(offscreen_canvas, 0, 0, 0, 63, color)
        graphics.DrawLine(offscreen_canvas, 63, 0, 63, 63, color)
        graphics.DrawLine(offscreen_canvas, 0, 63, 63, 63, color)
        offscreen_canvas = self.matrix.SwapOnVSync(offscreen_canvas)


# Main function
if __name__ == "__main__":
    jake = Jake()
    if (not jake.process()):
        jake.print_help()
