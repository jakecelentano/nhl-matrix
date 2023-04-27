#!/usr/bin/env python
from samplebase import SampleBase
from rgbmatrix import graphics
import time
from NHL import NHL
import datetime
from config import NHL_TEAMS
from PIL import Image

WHITE = graphics.Color(255, 255, 255)
class TeamsScreen(SampleBase):
    def __init__(self, *args, **kwargs):
        super(TeamsScreen, self).__init__(*args, **kwargs)
        self.nhl = NHL()
        #self.nba = NBA()
        #self.nfl = NFL()
        #self.mlb = MLB()
        self.teams = []
        self.color = graphics.Color(255, 255, 255)

    # main function
    def run(self):

        for team in NHL_TEAMS:
            self.teams.append(self.nhl.getTeam(team))
        
        print("Teams: " + str(self.teams))
        #for team in NBA_TEAMS:
        #    self.teams.append(self.nba.getTeam(team))
        #for team in NFL_TEAMS:
        #    self.teams.append(self.nfl.getTeam(team))
        #for team in MLB_TEAMS:
        #    self.teams.append(self.mlb.getTeam(team))

        # main loop
        sleep_time = 1
        next_games = [] # next games
        live_games = [] # live games or preview
        recently_finished_games = [] # gameId & timestamp from when game ended
        while True:
            time.sleep(sleep_time)
            try:
                # get the next game for each team
                for team in self.teams:
                    next_games.append(team.getNextGames(1)[0])

                # check if any games are live
                for game in next_games:
                    if game.isLive() or game.isPreview():
                        live_games.append(game)
                
                while len(live_games) > 0:
                    for game in live_games:
                        # cycle through live games
                        gameId = game.getId()
                        print(str(gameId) + ": " + str(game.getStatus() + " | " + game.getAwayTeamName() + " @ " + game.getHomeTeamName()) + " | " + str(game.getPeriod()) + " | " + str(game.getPeriodTime()))
                        offscreen_canvas = self.getLiveGameScreenNHL(game)
                        offscreen_canvas = self.matrix.SwapOnVSync(offscreen_canvas)
                        time.sleep(10)

                        # check if game is over
                        if game.isOver():
                            live_games.remove(game)
                            recently_finished_games.append([gameId, datetime.datetime.now()])
                            print("Game over: " + str(gameId))
                        
                        # show any recently finished games
                        for finished in recently_finished_games:
                            # remove games from recently_finished_games after 30 minutes
                            if (datetime.datetime.now() - finished[1]).total_seconds() > 1800:
                                recently_finished_games.remove(finished)
                                print("Removed game: " + str(finished[0]))
                            
                            offscreen_canvas = self.getLiveGameScreenNHL(finished[0])
                            offscreen_canvas = self.matrix.SwapOnVSync(offscreen_canvas)
                            time.sleep(8)
                
                # see how many seconds until the next game
                min_seconds_until_next_game = 1800
                for game in next_games:
                    print("Game: " + game.getStatus() + " | " + game.getAwayTeamName() + " @ " + game.getHomeTeamName() + " | " + str(game.getPeriod()) + " | " + str(game.getPeriodTime()))
                    seconds_until_next_game = game.getSecondsUntilNextGame()
                    print("Seconds until start " + str(seconds_until_next_game))
                    min_seconds_until_next_game = min(min_seconds_until_next_game, seconds_until_next_game)
                
                # sleep until the next game
                print("Sleeping for " + str(min_seconds_until_next_game-60) + " seconds")
                sleep_time = min_seconds_until_next_game-3600
                
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

    def getUpcomingGameScreenNHL(self, team):
        game = team.getNextGames(1)[0]
        offscreen_canvas = self.matrix.CreateFrameCanvas()
        self.drawBorder(team, offscreen_canvas)
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
    def getLiveGameScreenNHL(self, game):
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
