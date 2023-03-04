from nhl import NHL
from team import Team
import datetime

nhl = NHL(str(datetime.datetime.now().year))
for team in nhl.teams:
    print(team)
