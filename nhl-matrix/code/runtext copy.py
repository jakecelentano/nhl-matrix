#!/usr/bin/env python
# Display a runtext with double-buffering.
from samplebase import SampleBase
from rgbmatrix import graphics
import time


class RunText(SampleBase):
    def __init__(self, *args, **kwargs):
        super(RunText, self).__init__(*args, **kwargs)
        self.parser.add_argument("-t", "--text", help="The text to scroll on the RGB LED panel", default="Hello world!")

    def run(self):
        offscreen_canvas = self.matrix.CreateFrameCanvas()
        year = datetime.datetime.now().year
        nhl = NHL(year)
        print(year)
        for team in NHL_TEAMS:
            print(team)
            team = nhl.get_team_by_name(team)
            self.drawBorder(offscreen_canvas)
            self.drawLogo(offscreen_canvas, team=team)
            time.sleep(15)


# Main function
if __name__ == "__main__":
    run_text = RunText()
    if (not run_text.process()):
        print("Error processing arguments")
        run_text.print_help()
