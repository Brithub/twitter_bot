import os

import tweepy


def setup():
    # == OAuth Authentication ==
    #
    # This mode of authentication is the new preferred way
    # of authenticating with Twitter.

    # The consumer keys can be found on your application's Details
    # page located at https://dev.twitter.com/apps (under "OAuth settings")
    consumer_key=os.environ['CONSUMER_KEY']
    consumer_secret=os.environ['CONSUMER_SECRET']

    # The access tokens can be found on your applications's Details
    # page located at https://dev.twitter.com/apps (located
    # under "Your access token")
    access_token=os.environ['ACCESS_TOKEN']
    access_token_secret=os.environ['ACCESS_TOKEN_SECRET']

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    return tweepy.API(auth)


def write_tweet(text):
    api = setup()
    api.update_status(status=text)


def write_image_tweet(image_path, text):
    api = setup()
    api.update_with_media(image_path, text)
