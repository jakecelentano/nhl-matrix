from nhl import NHL
from team import Team
import datetime

nhl = NHL(str(datetime.datetime.now().year))
names = []
for team in nhl.teams:
    names.append(team.team_name)

names.sort()
# print the list one per line
for name in names:
    print(name)



