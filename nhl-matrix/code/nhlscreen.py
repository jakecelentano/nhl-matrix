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


        # loop
        sleep_time = 1
        while True:
            time.sleep(sleep_time)
            try:
                # get the next game (will include games today, so live games will be included)
                game = self.team.get_next_games(1)[0]
                # get id of the next game
                game_id = game.get_game_id()
                # check if game is live
                game_status = game.get_status()
                game_home_team = game.get_game_home_team_name()
                game_away_team = game.get_game_away_team_name()
                period = game.get_period()
                period_time = game.get_period_time()
                print(str(game_id) + ": " + str(game.get_status() + " | " + game_home_team + " vs " + game_away_team) + " | " + str(period) + " | " + str(period_time))

                if game_status == "Live" or game_status == "Final" or game_status == "In Progress":
                    # draw the live game screen
                    if game_status == "Live":
                        sleep_time = 5
                    elif game_status == "Final":
                        sleep_time = 1800
                    else:
                        sleep_time = 60
                    offscreen_canvas = self.getLiveGameScreen(game)
                    
                # get the next game
                else:
                    # get how many seconds between now and the next game
                    seconds_until_next_game = game.get_seconds_until_next_game()
                    print("Seconds until next game: " + str(seconds_until_next_game))
                    offscreen_canvas = self.getUpcomingGameScreen(game)
                    print("Drawing upcoming game screen")  
                    sleep_time = max(seconds_until_next_game-300, 60)

                offscreen_canvas = self.matrix.SwapOnVSync(offscreen_canvas) 
            except KeyboardInterrupt:
                print("Keyboard interrupt")
                break

    
    def drawBorder(self, offscreen_canvas=None):
        if offscreen_canvas is None:
            offscreen_canvas = self.matrix.CreateFrameCanvas()
        graphics.DrawLine(offscreen_canvas, 0, 0, 63, 0, self.color)
        graphics.DrawLine(offscreen_canvas, 0, 0, 0, 63, self.color)
        graphics.DrawLine(offscreen_canvas, 63, 0, 63, 63, self.color)
        graphics.DrawLine(offscreen_canvas, 0, 63, 63, 63, self.color)
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

        return offscreen_canvas

    # corner
    def getLiveGameScreen(self, game):
        offscreen_canvas = self.matrix.CreateFrameCanvas()
        font1 = graphics.Font()
        font1.LoadFont("fonts/texgyre-27.bdf")
        font2 = graphics.Font()
        font2.LoadFont("fonts/6x9.bdf")
        
        self.drawBorder(offscreen_canvas)   
        x, y = 1, 1
        home_team = self.nhl.get_team_by_id(game.get_game_home_team_id())
        away_team = self.nhl.get_team_by_id(game.get_game_away_team_id())

        LOGO_SIZE = 24
        home_team_logo = home_team.get_logo()
        home_team_logo = Image.open(home_team_logo)
        home_team_logo.thumbnail((LOGO_SIZE, LOGO_SIZE), Image.ANTIALIAS)
        home_team_logo = home_team_logo.convert('RGB')

        away_team_logo = away_team.get_logo()
        away_team_logo = Image.open(away_team_logo)
        away_team_logo.thumbnail((LOGO_SIZE, LOGO_SIZE), Image.ANTIALIAS)
        away_team_logo = away_team_logo.convert('RGB')

        # paste logos onto canvas
        offscreen_canvas.SetImage(home_team_logo, x+1, y+24)
        offscreen_canvas.SetImage(away_team_logo, x+1, y)

        # write score
        home_score = game.get_home_score()
        away_score = game.get_away_score()
        graphics.DrawText(offscreen_canvas, font1, x+36, y+22, graphics.Color(255, 255, 255), str(away_score))
        graphics.DrawText(offscreen_canvas, font1, x+36, y+46, graphics.Color(255, 255, 255), str(home_score))

        # write period and time
        if game.get_status() == "Final":
            period = "FINAL"
            period_time = ""
        elif game.get_status() == "Final/OT":
            period = "FINAL OT"
            period_time = ""
        else:
            period = str(game.get_period())
            if period == "0":
                period = "P"
            elif period == "1":
                period = "1st"
            elif period == "2":
                period = "2nd"
            elif period == "3":
                period = "3rd"
            elif period == "4":
                period = "OT"
            else:
                period = "?"
            period_time = str(game.get_period_time())

        graphics.DrawText(offscreen_canvas, font2, x+1, LOGO_SIZE*2 + 10, graphics.Color(255, 255, 255), period)
        graphics.DrawText(offscreen_canvas, font2, x+30, LOGO_SIZE*2 + 10, graphics.Color(255, 255, 255), period_time)

 


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
