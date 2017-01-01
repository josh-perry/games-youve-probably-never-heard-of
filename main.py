import random
import datetime as dt

from secrets import gb_api_key

from giantbomb import giantbomb

useragent = "Test"


def format_release_date(game):
    """ Formats the game's release date nicely. """
    d = game.original_release_date
    r = dt.datetime.strptime(d, "%Y-%m-%d 00:00:00")
    return dt.datetime.strftime(r, "%d %b %Y")


def get_platforms(game):
    """ Constructs a string containing the applicable platforms. """
    platforms = []

    for p in game.platforms:
        platforms.append(p["abbreviation"])

    return platforms


def get_credits(game):
    """ Constructs a string containing the developer/publisher names. """
    developer = game.developers[0]["name"]
    publisher = game.publishers[0]["name"]

    credit = " by " + game.developers[0]["name"]

    if developer != publisher:
        credit += "/" + publisher

    return credit


def main():
    # Init GiantBomb API with our key/useragent string
    gb = giantbomb.Api(gb_api_key, useragent)

    # TODO: Find a way to get the number of games in API
    # Get a random game
    game = gb.getGame(random.randint(1, 57500))

    # Get string for all platforms the game was released on
    platforms = get_platforms(game)

    # Dictionary for string formatting the tweet
    t = {"name": game.name,
         "release": format_release_date(game),
         "platforms": "/".join(platforms)}

    # Construct the tweet
    tweet = "{name} ({platforms}) released {release}".format(**t)

    # Get credits string for showing developer/publisher
    tweet += get_credits(game)

    print(tweet)


if __name__ == '__main__':
    retries = 10

    for i in range(retries):
        try:
            main()
            break
        except Exception, x:
            print("Error: " + x.message + ", retrying")
