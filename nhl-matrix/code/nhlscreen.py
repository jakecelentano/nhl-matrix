#!/usr/bin/env python
from samplebase import SampleBase
from rgbmatrix import graphics
import time
from nhl import NHL
from team import Team
import datetime
from config import DEFAULT_TEAM
from PIL import Image



class NHLScreen(SampleBase):
    def __init__(self, *args, **kwargs):
        super(NHLScreen, self).__init__(*args, **kwargs)
        self.parser.add_argument("-t", "--team", help="The team to display", default=DEFAULT_TEAM)
        self.nhl = NHL(str(datetime.datetime.now().year))
        self.team = "No team"
        self.color = graphics.Color(255, 255, 255)


    # main function
    def run(self):
        # start
        team = self.args.team
        self.team = self.nhl.get_team_by_name(team)
        if self.team is None:
            print("Team not found: " + team)
            return

        team_primary_color = self.team.get_primary_color()
        self.color = graphics.Color(team_primary_color[0], team_primary_color[1], team_primary_color[2])

        # get the next game
        game = self.team.get_next_games(1)[0]
        # get id of the next game
        game_id = game.get_game_id()

        # draw the upcoming game screen
        #offscreen_canvas = self.getUpcomingGameScreen(game)
        offscreen_canvas = self.getScoreboardScreen(game)
        print("Drawing upcoming game screen")
        offscreen_canvas = self.matrix.SwapOnVSync(offscreen_canvas)
        
        while True:
            time.sleep(10)
            # wait for keyboard interrupt
            try:
                # get the next game
                game = self.team.get_next_games(1)[0]
                # get id of the next game
                new_game_id = game.get_game_id()
                if new_game_id != game_id:
                    game_id = new_game_id
                    # draw the new upcoming game screen
                    offscreen_canvas = self.getUpcomingGameScreen(game)
                    offscreen_canvas = self.matrix.SwapOnVSync(offscreen_canvas)
                else:
                    pass
            except KeyboardInterrupt:
                print("Keyboard interrupt")
                break

    
    def drawBorder(self, offscreen_canvas=None):
        color = self.color
        if offscreen_canvas is None:
            offscreen_canvas = self.matrix.CreateFrameCanvas()
        graphics.DrawLine(offscreen_canvas, 0, 0, 63, 0, color)
        graphics.DrawLine(offscreen_canvas, 0, 0, 0, 63, color)
        graphics.DrawLine(offscreen_canvas, 63, 0, 63, 63, color)
        graphics.DrawLine(offscreen_canvas, 0, 63, 63, 63, color)
        #offscreen_canvas = self.matrix.SwapOnVSync(offscreen_canvas)

    def getUpcomingGameScreen(self, game):
        offscreen_canvas = self.matrix.CreateFrameCanvas()
        self.drawBorder(offscreen_canvas)
        font = graphics.Font()
        font.LoadFont("fonts/5x8.bdf")
        
        x, y = 2, 2
        home_team = self.nhl.get_team_by_id(game.get_game_home_team_id())
        away_team = self.nhl.get_team_by_id(game.get_game_away_team_id())
        # get logo paths
        home_team_logo = home_team.get_logo()
        away_team_logo = away_team.get_logo()
        # convert to 30x30 PIL images in RGB
        home_team_logo = Image.open(home_team_logo)
        home_team_logo.thumbnail((24, 24), Image.ANTIALIAS)
        home_team_logo = home_team_logo.convert('RGB')
        away_team_logo = Image.open(away_team_logo)
        away_team_logo.thumbnail((24, 24), Image.ANTIALIAS)
        away_team_logo = away_team_logo.convert('RGB')
        # paste logos onto canvas
        offscreen_canvas.SetImage(home_team_logo, x, y)
        offscreen_canvas.SetImage(away_team_logo, x+36, y)

        # draw vs between logos
        graphics.DrawText(offscreen_canvas, font, x+27, y+16, graphics.Color(255, 255, 255), "@") # 27 + 5 = 32 (offset + font width = center)
        
        #YYYY-MM-DD
        game_date =  game.get_game_date()
        #HH:MM AM/PM
        game_time = game.get_game_time_pretty()
        game_day_of_week = game.get_game_day_of_week()
        current_date = self.getCurrentDate() # YYYY-MM-DD
        if game_date == current_date:
            game_day_of_week = "Today"
            if int(game_time.split(":")[0]) >= 7: # if game is at 7pm or later
                game_day_of_week = "Tonight"


        # draw day of week
        graphics.DrawText(offscreen_canvas, font, x+2, y+32, graphics.Color(255, 255, 255), game_day_of_week)
        # draw @ time
        graphics.DrawText(offscreen_canvas, font, x+2, y+40, graphics.Color(255, 255, 255), "@ " + game_time)

    # corner
    def getScoreboardScreen(self, game):
        offscreen_canvas = self.matrix.CreateFrameCanvas()
        font = graphics.Font()
        
        
        x, y = 2, 2
        home_team = self.nhl.get_team_by_id(game.get_game_home_team_id())
        away_team = self.nhl.get_team_by_id(game.get_game_away_team_id())

        home_team_logo = home_team.get_logo()
        home_team_logo = Image.open(home_team_logo)
        home_team_logo.thumbnail((48, 48), Image.ANTIALIAS)
        home_team_logo = home_team_logo.convert('RGB')

        away_team_logo = away_team.get_logo()
        away_team_logo = Image.open(away_team_logo)
        away_team_logo.thumbnail((48, 48), Image.ANTIALIAS)
        away_team_logo = away_team_logo.convert('RGB')

        

        offscreen_canvas.SetImage(home_team_logo, x-30, y-20)
        offscreen_canvas.SetImage(home_team_logo, x+30, y-20)

        return offscreen_canvas
    
    def getCurrentDate(self):
        now = datetime.datetime.now()
        year = now.year
        month = now.month
        day = now.day

        if month < 10:
            month = "0" + str(month)
        if day < 10:
            day = "0" + str(day)
        
        return str(year) + "-" + str(month) + "-" + str(day)
        
        





# Main function
if __name__ == "__main__":
    screen = NHLScreen()
    if (not screen.process()):
        screen.print_help()
