#!/usr/bin/env python
from samplebase import SampleBase
from rgbmatrix import graphics
import time
from nhl import NHL
from team import Team
import datetime
from config import DEFAULT_TEAM



class NHLScreen(SampleBase):
    def __init__(self, *args, **kwargs):
        super(NHLScreen, self).__init__(*args, **kwargs)

    # main function
    def run(self):
        offscreen_canvas = self.matrix.CreateFrameCanvas()
        nhl = NHL(str(datetime.datetime.now().year))
        team = nhl.get_team_by_name(DEFAULT_TEAM)
        team_primary_color = team.get_primary_color()
        print(team_primary_color)
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

    def drawUpcomingGamesScreen(self, team):
        offscreen_canvas = self.matrix.CreateFrameCanvas()
        font = graphics.Font()
        font.LoadFont("fonts/7x13.bdf")
        textColor = graphics.Color(255, 255, 0)
        pos = offscreen_canvas.width
        my_text = self.args.text

        while True:
            offscreen_canvas.Clear()
            len = graphics.DrawText(offscreen_canvas, font, pos, 10, textColor, my_text)
            pos -= 1
            if (pos + len < 0):
                pos = offscreen_canvas.width

            time.sleep(0.05)
            offscreen_canvas = self.matrix.SwapOnVSync(offscreen_canvas)


# Main function
if __name__ == "__main__":
    screen = NHLScreen()
    if (not screen.process()):
        screen.print_help()
