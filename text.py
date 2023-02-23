from samplebase import SampleBase
from rgbmatrix import graphics
import time


class ShowText(SampleBase):
    def __init__(self, *args, **kwargs):
        super(ShowText, self).__init__(*args, **kwargs)
        self.parser.add_argument("-t", "--text", help="The text to show", default="Hello world!")

    def run(self):
        offscreen_canvas = self.matrix.CreateFrameCanvas()
        font = graphics.Font()
        font.LoadFont("fonts/7x13.bdf")
        textColor = graphics.Color(255, 255, 0)
        pos = offscreen_canvas.width
        my_text = self.args.text

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
            my_text = word
            offscreen_canvas.Clear()
            # DrawText(Canvas, Font, x, y, color, text);
            len = graphics.DrawText(offscreen_canvas, font, pos, 10, textColor, my_text)
            print(len)
            time.sleep(5)
            offscreen_canvas = self.matrix.SwapOnVSync(offscreen_canvas)



def main():
    my_text = ShowText()
    if (not my_text.process()):
        my_text.print_help()








if __name__ == "__main__":
    main()

