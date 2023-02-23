from nhl import NHL
import datetime

def main():
    # get current year
    year = datetime.datetime.now().year
    nhl = NHL(year)

    # get schedule for next 7 days
    start_date = datetime.datetime.now().strftime("%Y-%m-%d")
    end_date = (datetime.datetime.now() + datetime.timedelta(days=14)).strftime("%Y-%m-%d")
    #nhl_schedule = nhl.get_schedule(start_date, end_date)

    bruins = nhl.get_team_by_name("Boston Bruins")
    next_games = bruins.get_next_games(2)
    for x, game in enumerate(next_games):
        print(x+1)
        game.pretty_print()

    bruins_logo = bruins.get_logo()
    # show the image in a window
    




if __name__ == '__main__':
    main()