from samplebase import SampleBase
from rgbmatrix import graphics
import time
from nhl import NHL
from team import Team
from PIL import Image
import datetime
from config import DEFAULT_FONT, DEFAULT_FONT_COLOR, DEFAULT_TEAM




class NHLScreen(SampleBase):
    def __init__(self, *args, **kwargs):
        super(NHLScreen, self).__init__(*args, **kwargs)
        self.matrix = super(NHLScreen, sefl).get_matrix()
        self.nhl = NHL(str(datetime.datetime.now().year))


        
    def drawUpcomingGamesScreen(self, team):
        offscreen_canvas = self.matrix.CreateFrameCanvas()
        font = graphics.Font()
        font.LoadFont(DEFAULT_FONT)
        color = graphics.Color(DEFAULT_FONT_COLOR[0], DEFAULT_FONT_COLOR[1], DEFAULT_FONT_COLOR[2])
        x = 2
        y = 2   
        team_color = graphics.Color(team.get_primary_color()[0], team.get_primary_color()[1], team.get_primary_color()[2])
        

        games = team.get_next_games(2)
        team 

        for game in games:
            home_team = self.nhl.get_team_by_id(game.get_game_home_team_id())
            away_team = self.nhl.get_team_by_id(game.get_game_away_team_id())
            # get logo paths
            home_team_logo = home_team.get_logo()
            away_team_logo = away_team.get_logo()
            # convert to 30x30 PIL images in RGB
            home_team_logo = Image.open(home_team_logo)
            home_team_logo.thumbnail((30, 30), Image.ANTIALIAS)
            home_team_logo = home_team_logo.convert('RGB')
            away_team_logo = Image.open(away_team_logo)
            away_team_logo.thumbnail((30, 30), Image.ANTIALIAS)
            away_team_logo = away_team_logo.convert('RGB')
            # paste logos onto canvas
            offscreen_canvas.SetImage(home_team_logo, x, y)
            offscreen_canvas.SetImage(away_team_logo, x+30, y)
            # draw team names
            graphics.DrawText(offscreen_canvas, self.font, x, y+30, team_color, home_team.get_name())
            graphics.DrawText(offscreen_canvas, self.font, x+30, y+30, team_color, away_team.get_name())
            # draw game time
            game_time = game.get_game_time()
            game_time = game_time.strftime("%I:%M %p")
            graphics.DrawText(offscreen_canvas, self.font, x, y+45, team_color, game_time)
            y += 30
        offscreen_canvas = self.matrix.SwapOnVSync(offscreen_canvas)

    def drawBorder(self):
        graphics.DrawLine(offscreen_canvas, 0, 0, 63, 0, self.color)
        graphics.DrawLine(offscreen_canvas, 0, 0, 0, 63, self.color)
        graphics.DrawLine(offscreen_canvas, 63, 0, 63, 63, self.color)
        graphics.DrawLine(offscreen_canvas, 0, 63, 63, 63, self.color)
        offscreen_canvas = self.matrix.SwapOnVSync(offscreen_canvas)

