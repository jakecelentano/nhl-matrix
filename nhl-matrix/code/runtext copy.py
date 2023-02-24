#!/usr/bin/env python
# Display a runtext with double-buffering.
from samplebase import SampleBase
from rgbmatrix import graphics
import time
from nhl import NHL
from team import Team


class RunText(SampleBase):
    def __init__(self, *args, **kwargs):
        super(RunText, self).__init__(*args, **kwargs)
        self.parser.add_argument("-t", "--text", help="The text to scroll on the RGB LED panel", default="Hello world!")

    def run(self):
        year = 2023
        nhl = NHL(year)
        team = Team(nhl, 'Boston Bruins')
        offscreen_canvas = self.matrix.CreateFrameCanvas()
        font = graphics.Font()
        font.LoadFont("fonts/7x13.bdf")
        textColor = graphics.Color(255, 255, 0)
        pos = offscreen_canvas.width
        my_text = self.args.text    
        try:
            logo = team.get_logo()
        except:
            logo = 'images/nhl.png'
        x = 5
        y = 5
        offscreen_canvas.SetImage(logo, x, y)
        offscreen_canvas = self.matrix.SwapOnVSync(offscreen_canvas)
        time.sleep(10)


# Main function
if __name__ == "__main__":
    run_text = RunText()
    if (not run_text.process()):
        print("Error processing arguments")
        run_text.print_help()
