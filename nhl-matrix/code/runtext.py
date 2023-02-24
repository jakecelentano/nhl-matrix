#!/usr/bin/env python
# Display a runtext with double-buffering.
from samplebase import SampleBase
from rgbmatrix import graphics
import time
from team import Team
from nhl import NHL
import datetime
from setup import NHL_TEAMS


# def DrawLine(core.Canvas c, int x1, int y1, int x2, int y2, Color color):
# def DrawCircle(core.Canvas c, int x, int y, int radius, Color color):
# def DrawRectangle(core.Canvas c, int x, int y, int width, int height, Color color):
# def DrawText(core.Canvas c, Font font, int x, int y, Color color, string text):

BRUINS_YELLOW = graphics.Color(253, 185, 39)
BRUINS_BLACK = graphics.Color(0, 0, 0)



class RunText(SampleBase):
    def __init__(self, *args, **kwargs):
        super(RunText, self).__init__(*args, **kwargs)
        self.parser.add_argument("-t", "--text", help="The text to scroll on the RGB LED panel", default="Hello world!")

    def run(self):
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

    def drawText(self, offscreen_canvas, x=2, y=6, font="fonts/4x6.bdf", textColor=BRUINS_YELLOW, my_text="text"):
        textfont = graphics.Font()
        font = textfont.LoadFont("fonts/4x6.bdf")
        textColor = graphics.Color(255, 255, 255)
        my_text = self.args.text
        len = graphics.DrawText(offscreen_canvas, font, x, y, textColor, my_text)
        x = 0
        y = 4
        offscreen_canvas.Clear()
        self.drawBorder(offscreen_canvas)
        my_text = "text"
        len = graphics.DrawText(offscreen_canvas, font, x, y, textColor, my_text)
        offscreen_canvas = self.matrix.SwapOnVSync(offscreen_canvas)

    def drawLogo(self, offscreen_canvas, x=0, y=4, team=None):
        # offscreen_canvas.Clear()
        try:
            logo = team.get_logo()
        except:
            logo = 'images/nhl.png'
        offscreen_canvas.SetImage(logo, x, y)
        offscreen_canvas = self.matrix.SwapOnVSync(offscreen_canvas)



    def drawBorder(self, offscreen_canvas):
        graphics.DrawLine(offscreen_canvas, 0, 0, 63, 0, BRUINS_YELLOW)
        graphics.DrawLine(offscreen_canvas, 0, 0, 0, 63, BRUINS_YELLOW)
        graphics.DrawLine(offscreen_canvas, 63, 0, 63, 63, BRUINS_YELLOW)
        graphics.DrawLine(offscreen_canvas, 0, 63, 63, 63, BRUINS_YELLOW)


# Main function
if __name__ == "__main__":
    run_text = RunText()
    if (not run_text.process()):
        print("Error processing arguments")
        run_text.print_help()
