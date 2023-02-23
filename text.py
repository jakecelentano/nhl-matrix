from samplebase import SampleBase
from rgbmatrix import graphics
import time

BRUINS_YELLOW = graphics.Color(253, 185, 39)
BRUINS_BLACK = graphics.Color(0, 0, 0)

#def DrawLine(core.Canvas c, int x1, int y1, int x2, int y2, Color color):
#def DrawCircle(core.Canvas c, int x, int y, int radius, Color color):
#def DrawRectangle(core.Canvas c, int x, int y, int width, int height, Color color):
#def DrawText(core.Canvas c, Font font, int x, int y, Color color, string text):

class ShowText(SampleBase):
    def __init__(self, *args, **kwargs):
        super(ShowText, self).__init__(*args, **kwargs)
        self.parser.add_argument("-t", "--text", help="The text to show", default="Hello world!")

    def run(self):
        offscreen_canvas = self.matrix.CreateFrameCanvas()
        font = graphics.Font()
        font.LoadFont("fonts/4x6.bdf")
        textColor = graphics.Color(255, 255, 0)
        my_text = self.args.text
        x = 0
        y = 4

        words_list = ['apple', 
                      'banana',
                      'orange',
                      'grape',
                      'watermelon',
                      'pineapple',
                      'strawberry',
                      'blueberry',
                      'raspberry',
                      'blackberry']
        
        for word in words_list:
            print(x, y)
            my_text = word
            offscreen_canvas.Clear()
            self.drawBorder(offscreen_canvas)
            len = graphics.DrawText(offscreen_canvas, font, x, y, textColor, my_text)
            print(len)
            offscreen_canvas = self.matrix.SwapOnVSync(offscreen_canvas)
            time.sleep(5)
            x += 5
            #y += 5


    def drawBorder(self, offscreen_canvas):
        graphics.DrawLine(offscreen_canvas, 0, 0, 63, 0, BRUINS_YELLOW)
        graphics.DrawLine(offscreen_canvas, 0, 0, 0, 63, BRUINS_YELLOW)
        graphics.DrawLine(offscreen_canvas, 63, 0, 63, 63, BRUINS_YELLOW)
        graphics.DrawLine(offscreen_canvas, 0, 63, 63, 63, BRUINS_YELLOW)




def main():
    my_text = ShowText()
    if (not my_text.process()):
        my_text.print_help()








if __name__ == "__main__":
    main()

