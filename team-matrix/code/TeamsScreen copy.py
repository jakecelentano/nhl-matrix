#!/usr/bin/env python
from samplebase import SampleBase
from rgbmatrix import graphics
import time
from NHL import NHL
from NHLTeam import NHLTeam
import datetime
from config import NHL_TEAMS
from PIL import Image

WHITE = graphics.Color(255, 255, 255)

class TeamsScreen(SampleBase):
    def __init__(self, *args, **kwargs):
        super(TeamsScreen, self).__init__(*args, **kwargs)
        #self.parser.add_argument("-t", "--team", help="The team to display", default=DEFAULT_TEAM)
        self.nhl = NHL()
        self.teams = []
        self.color = graphics.Color(255, 255, 255)


    # main function
    def run(self):
        #team = self.args.team
        for team in NHL_TEAMS:
            self.teams.append(self.nhl.getTeam(team))

        team_primary_color = self.team.getPrimaryColor()
        self.color = graphics.Color(team_primary_color[0], team_primary_color[1], team_primary_color[2])

        # main loop
        sleep_time = 1
        while True:
            time.sleep(sleep_time)
            try:
                # get the next game (will include games today, so live games will be included)
                game = self.team.getNextGames(1)[0]
                # get id of the next game
                game_id = game.getId()
                # check if game is live
                status = game.getStatus()
                homeTeam = game.getHomeTeamName()
                awayTeam = game.getAwayTeamName()
                try:
                    period = game.getPeriod()
                    period_time = game.getPeriodTime()
                except:
                    period = "N/A"
                    period_time = "N/A"
                print(str(game_id) + ": " + str(status + " | " + awayTeam + " @ " + homeTeam) + " | " + str(period) + " | " + str(period_time))

                if status == "Live" or status == "Final" or status == "In Progress":
                    # draw the live game screen
                    if status == "Live":
                        sleep_time = 5
                    elif status == "Final":
                        sleep_time = 1800
                    else:
                        sleep_time = 60
                    offscreen_canvas = self.getLiveGameScreen(game)
                    
                # get the next game
                else:
                    # get how many seconds between now and the next game
                    seconds_until_next_game = game.getSecondsUntilNextGame()
                    print("Seconds until next game: " + str(seconds_until_next_game))
                    offscreen_canvas = self.getUpcomingGameScreen(team)
                    print("Drawing upcoming game screen")  
                    sleep_time = min(abs(seconds_until_next_game-300), 3600)
                    if seconds_until_next_game <= 300:
                        sleep_time = 300

                offscreen_canvas = self.matrix.SwapOnVSync(offscreen_canvas) 
            except KeyboardInterrupt:
                print("Keyboard interrupt")
                break

    
    def drawBorder(self, team, offscreen_canvas=None):
        team_primary_color = team.getPrimaryColor()
        color = graphics.Color(team_primary_color[0], team_primary_color[1], team_primary_color[2])

        if offscreen_canvas is None:
            offscreen_canvas = self.matrix.CreateFrameCanvas()
        graphics.DrawLine(offscreen_canvas, 0, 0, 63, 0, color)
        graphics.DrawLine(offscreen_canvas, 0, 0, 0, 63, color)
        graphics.DrawLine(offscreen_canvas, 63, 0, 63, 63, color)
        graphics.DrawLine(offscreen_canvas, 0, 63, 63, 63, color)
        #offscreen_canvas = self.matrix.SwapOnVSync(offscreen_canvas)

    def getUpcomingGameScreen(self, team):

        offscreen_canvas = self.matrix.CreateFrameCanvas()
        self.drawBorder(offscreen_canvas)
        font = graphics.Font()
        font.LoadFont("fonts/5x8.bdf")
        font_width = 5
        
        x, y = 2, 2
        home_team = self.nhl.getTeam(game.getHomeTeamId())
        away_team = self.nhl.getTeam(game.getAwayTeamId())
        # get logo paths
        home_team_logo = home_team.getLogo()
        away_team_logo = away_team.getLogo()
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
        graphics.DrawText(offscreen_canvas, font, x+27, y+16, WHITE, "@") # 27 + 5 = 32 (offset + font width = center)
        
        #YYYY-MM-DD
        game_date =  game.getDate()
        #HH:MM AM/PM
        game_time = game.getTimePretty()
        game_day_of_week = game.getDayOfWeek()
        current_date = self.getCurrentDate() # YYYY-MM-DD
        if game_date == current_date:
            game_day_of_week = "Today"
            if int(game_time.split(":")[0]) >= 7: # if game is at 7pm or later
                game_day_of_week = "Tonight"

        tomorrow = datetime.timedelta(days=1) + datetime.datetime.now()
        tomorrow = tomorrow.strftime("%Y-%m-%d")
        if game_date == tomorrow:
            game_day_of_week = "Tomorrow"
        

        # draw day of week
        graphics.DrawText(offscreen_canvas, font, x+2, y+32, WHITE, game_day_of_week)
        # draw @ time
        graphics.DrawText(offscreen_canvas, font, x+2, y+40, WHITE, "@ " + game_time)

        # draw abbrevations + win/loss record
        home_wins = home_team.getWins()
        home_losses = home_team.getLosses()
        home_ot = home_team.getOT()
        away_wins = away_team.getWins()
        away_losses = away_team.getLosses()
        away_ot = away_team.getOT()
        home_primary_color = home_team.getPrimaryColor()
        away_primary_color = away_team.getPrimaryColor()
        home_color = graphics.Color(home_primary_color[0], home_primary_color[1], home_primary_color[2])
        away_color = graphics.Color(away_primary_color[0], away_primary_color[1], away_primary_color[2])
        graphics.DrawText(offscreen_canvas, font, x+2, y+50, home_color, home_team.getAbbreviation() )
        graphics.DrawText(offscreen_canvas, font, x+2, y+58, away_color, away_team.getAbbreviation() )
        # draw wins - losses - ot
        graphics.DrawText(offscreen_canvas, font, x+font_width*len(home_team.getAbbreviation())+6, y+50, WHITE, str(home_wins) + "-" + str(home_losses) + "-" + str(home_ot))
        graphics.DrawText(offscreen_canvas, font, x+font_width*len(away_team.getAbbreviation())+6, y+58, WHITE, str(away_wins) + "-" + str(away_losses) + "-" + str(away_ot))



      

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
        home_team = self.nhl.getTeam(game.getHomeTeamId())
        away_team = self.nhl.getTeeam(game.getAwayTeamId())

        LOGO_SIZE = 24
        home_team_logo = home_team.getLogo()
        home_team_logo = Image.open(home_team_logo)
        home_team_logo.thumbnail((LOGO_SIZE, LOGO_SIZE), Image.ANTIALIAS)
        home_team_logo = home_team_logo.convert('RGB')

        away_team_logo = away_team.getLogo()
        away_team_logo = Image.open(away_team_logo)
        away_team_logo.thumbnail((LOGO_SIZE, LOGO_SIZE), Image.ANTIALIAS)
        away_team_logo = away_team_logo.convert('RGB')

        # paste logos onto canvas
        offscreen_canvas.SetImage(home_team_logo, x+1, y+24)
        offscreen_canvas.SetImage(away_team_logo, x+1, y)

        # write score
        home_score = game.getHomeScore()
        away_score = game.getAwayScore()
        graphics.DrawText(offscreen_canvas, font1, x+36, y+22, WHITE, str(away_score))
        graphics.DrawText(offscreen_canvas, font1, x+36, y+46, WHITE, str(home_score))

        # write period and time
        if game.getStatus() == "Final":
            period = "FINAL"
            period_time = ""
        elif game.getStatus() == "Final/OT":
            period = "FINAL OT"
            period_time = ""
        else:
            period = str(game.getPeriod())
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
            period_time = str(game.getPeriodTime())

        graphics.DrawText(offscreen_canvas, font2, x+1, LOGO_SIZE*2 + 10, WHITE, period)
        graphics.DrawText(offscreen_canvas, font2, x+30, LOGO_SIZE*2 + 10, WHITE, period_time)

 


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
    screen = TeamsScreen()
    if (not screen.process()):
        screen.print_help()
