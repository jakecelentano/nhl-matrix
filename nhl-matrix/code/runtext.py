#!/usr/bin/env python
# Display a runtext with double-buffering.
from samplebase import SampleBase
from rgbmatrix import graphics
import time
from nhl import NHL
from team import Team
from PIL import Image


BRUINS_YELLOW = graphics.Color(253, 185, 39)
BRUINS_BLACK = graphics.Color(0, 0, 0)

class RunText(SampleBase):
    def __init__(self, *args, **kwargs):
        super(RunText, self).__init__(*args, **kwargs)
        self.parser.add_argument("-t", "--text", help="The text to scroll on the RGB LED panel", default="Hello world!")

    def run(self):
        offscreen_canvas = self.matrix.CreateFrameCanvas()
        #font = graphics.Font()
        #font.LoadFont("fonts/4x6.bdf")
        #textColor = graphics.Color(255, 255, 0)
        #pos = offscreen_canvas.width
        #my_text = self.args.text
        year = 2023
        nhl = NHL(year)
        bruins = nhl.get_team_by_name("Boston Bruins")
        self.drawLogo(offscreen_canvas, team=bruins)
        self.drawBorder(offscreen_canvas)
        time.sleep(15)
        
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
    
    def drawLogo(self, offscreen_canvas, x=4, y=4, team=None):
        logo = 'logos/Boston Bruins.png'
        image = Image.open(logo)
        image.thumbnail((56, 56), Image.ANTIALIAS)
        image = image.convert('RGB')
        offscreen_canvas.SetImage(image, x, y)
        offscreen_canvas = self.matrix.SwapOnVSync(offscreen_canvas)

    def drawBorder(self, offscreen_canvas):
        graphics.DrawLine(offscreen_canvas, 0, 0, 63, 0, BRUINS_YELLOW)
        graphics.DrawLine(offscreen_canvas, 0, 0, 0, 63, BRUINS_YELLOW)
        graphics.DrawLine(offscreen_canvas, 63, 0, 63, 63, BRUINS_YELLOW)
        graphics.DrawLine(offscreen_canvas, 0, 63, 63, 63, BRUINS_YELLOW)
        offscreen_canvas = self.matrix.SwapOnVSync(offscreen_canvas)


# Main function
if __name__ == "__main__":
    run_text = RunText()
    if (not run_text.process()):
        print("Error processing arguments")
        run_text.print_help()
