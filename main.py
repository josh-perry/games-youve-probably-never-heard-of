import os
import random
import datetime as dt
import urllib
import urlparse

from secrets import *

from giantbomb import giantbomb
import tweepy

useragent = "Test"

# Maximum number of images to download
max_images = 4


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


def save_images(game):
    base_path = "./cache/{}/".format(game.id)
    image_paths = []

    download_count = 0

    if not os.path.exists(base_path):
        os.makedirs(base_path)

    for i in xrange(len(game.images)):
        if download_count >= max_images:
            break

        try:
            image = game.images[i]

            url = image["super_url"]

            url_path = urlparse.urlparse(url).path
            ext = os.path.splitext(url_path)[1]

            path = base_path + str(i) + ext
            urllib.urlretrieve(url, path)

            image_paths.append(path)
            download_count += 1
        except:
            continue

    return image_paths


def get_game():
    # Init GiantBomb API with our key/useragent string
    gb = giantbomb.Api(gb_api_key, useragent)

    # TODO: Find a way to get the number of games in API
    # Get a random game
    game = gb.getGame(random.randint(1, 57500))

    return game


def create_tweet(game):
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

    return tweet


def post_tweet(tweet, images):
    # Set up Twitter stuff
    twitter_auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    twitter_auth.set_access_token(access_key, access_secret)
    twitter_api = tweepy.API(twitter_auth)

    # Upload media + get IDs for the status
    media_ids = [twitter_api.media_upload(i).media_id_string for i in images]

    # Post tweet!
    twitter_api.update_status(status=tweet, media_ids=media_ids)


if __name__ == '__main__':
    retries = 10

    for i in range(retries):
        try:
            game = get_game()
            tweet = create_tweet(game)
            post_tweet(tweet, save_images(game))
            break
        except x:
            print("Error: " + x.message + ", retrying")
