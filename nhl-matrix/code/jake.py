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
        font = graphics.Font()
        font.LoadFont("fonts/4x6.bdf")
        graphics.DrawLine(offscreen_canvas, 0, 0, 63, 0, self.color)
        graphics.DrawLine(offscreen_canvas, 0, 0, 0, 63, self.color)
        graphics.DrawLine(offscreen_canvas, 63, 0, 63, 63, self.color)
        graphics.DrawLine(offscreen_canvas, 0, 63, 63, 63, self.color)
        offscreen_canvas = self.matrix.SwapOnVSync(offscreen_canvas)

        while True:
            offscreen_canvas = self.matrix.SwapOnVSync(offscreen_canvas)


# Main function
if __name__ == "__main__":
    jake = Jake()
    if (not jake.process()):
        jake.print_help()
