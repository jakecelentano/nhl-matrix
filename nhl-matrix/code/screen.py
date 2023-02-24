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



class Screen(SampleBase):
    def __init__(self, *args, **kwargs):
        super(Screen, self).__init__(*args, **kwargs)
        self.parser.add_argument("-t", "--text", help="The text to show", default="Hello world!")

    def run(self):
        offscreen_canvas = self.matrix.CreateFrameCanvas()
        year = datetime.datetime.now().year
        nhl = NHL(year)
        for team in NHL_TEAMS:
            team = nhl.get_team_by_name(team)
            self.drawBorder(offscreen_canvas)
            self.drawLogo(offscreen_canvas, team=team)
            time.sleep(15)
            
        #bruins = nhl.get_team_by_name("Boston Bruins")
        #next_games = bruins.get_next_games(2)
        #self.drawLogo(offscreen_canvas, team=bruins)


        
        time.sleep(5)

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
    scr = Screen()
    if (not scr.process()):
        print("Error processing arguments")
        scr.print_help()
