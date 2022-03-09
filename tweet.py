import os

import tweepy


def setup():
    consumer_key = os.environ['CONSUMER_KEY']
    consumer_secret = os.environ['CONSUMER_SECRET']
    access_token = os.environ['ACCESS_TOKEN']
    access_token_secret = os.environ['ACCESS_TOKEN_SECRET']

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    return tweepy.API(auth)


def write_tweet(text):
    api = setup()
    api.update_status(status=text)


def write_image_tweet(image_path, text):
    api = setup()
    api.update_status_with_media(text, image_path)

def update_image(path):
    spi = setup()
    spi.update_profile_image(path)