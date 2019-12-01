#!/usr/bin/env python
# encoding: utf-8
# Taken from https://github.com/marado/tweet_dumper with minimum case-specific modifications

import tweepy  # https://github.com/tweepy/tweepy
import clean_text
import os

# Twitter API credentials
consumer_key = os.environ['CONSUMER_KEY']
consumer_secret = os.environ['CONSUMER_SECRET']
access_token = os.environ['ACCESS_TOKEN']
access_token_secret = os.environ['ACCESS_TOKEN_SECRET']


def get_all_tweets(screen_name):

    # authorize twitter, initialize tweepy
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    # initialize a list to hold all the tweepy Tweets
    all_tweets = []

    # make initial request for most recent tweets (200 is the maximum allowed count)
    new_tweets = api.user_timeline(screen_name=screen_name, count=200,tweet_mode = 'extended')

    # save most recent tweets
    all_tweets.extend(new_tweets)

    # save the id of the oldest tweet less one
    oldest = all_tweets[-1].id - 1

    # keep grabbing tweets until there are no tweets left to grab
    while len(new_tweets) > 750:
        print ("getting tweets before %s" % (oldest))

        # all subsequent requests use the max_id param to prevent duplicates
        new_tweets = api.user_timeline(screen_name=screen_name, count=200, max_id=oldest)

        # save most recent tweets
        all_tweets.extend(new_tweets)

        # update the id of the oldest tweet less one
        oldest = all_tweets[-1].id - 1

        print("...%s tweets downloaded so far" % (len(all_tweets)))

    clean = open(f"/tmp/{screen_name}-clean.txt", "a")
    for tweet in all_tweets:
        if hasattr(tweet, "full_text"):
            cleaned = clean_text.clean_text(tweet.full_text)
        else:
            cleaned = clean_text.clean_text(tweet.text)
        if cleaned != "":
            clean.write(cleaned + "\n")

    pass
