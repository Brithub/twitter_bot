#!/usr/bin/env python
# encoding: utf-8
# Taken from https://github.com/marado/tweet_dumper with minimum case-specific modifications

import datetime
import logging
import os

import tweepy  # https://github.com/tweepy/tweepy

from utils import delete_blob, upload_blob, get_blob
from utils import get_bad_phrases, clean_text

# Twitter API credentials
consumer_key = os.environ['CONSUMER_KEY']
consumer_secret = os.environ['CONSUMER_SECRET']
access_token = os.environ['ACCESS_TOKEN']
access_token_secret = os.environ['ACCESS_TOKEN_SECRET']
bucket = os.environ['BUCKET']

temp_path = "/tmp/badwords.txt"
key = "badwords.txt"
people = ["bijanmustard", "7e5h", "dadurath", "armaan__zi", "theonion", "clickhole"]


def downloader_function(thing, thing2):
    hour = int((datetime.datetime.utcnow() - datetime.datetime(1970, 1, 1)).total_seconds() / 3600)
    who = people[hour % len(people)]
    full = get_all_tweets(who)
    tweet_count = len(full.split('\n'))
    logging.info(f"Got {tweet_count} tweets")
    upload_blob("twitter_bot_bucket", f"/tmp/{who}-clean.txt", f"{who}-clean.txt")
    return f"Got and wrote {tweet_count} tweets for {who}"


def get_all_tweets(screen_name):
    # authorize twitter, initialize tweepy
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    # initialize a list to hold all the tweepy Tweets
    all_tweets = []

    # make initial request for most recent tweets (200 is the maximum allowed count)
    new_tweets = api.user_timeline(screen_name=screen_name, count=200, tweet_mode='extended')

    # save most recent tweets
    all_tweets.extend(new_tweets)

    # save the id of the oldest tweet less one
    oldest = all_tweets[-1].id - 1

    # keep grabbing tweets until there are no tweets left to grab
    while len(all_tweets) < 300:
        print("getting tweets before %s" % (oldest))

        # all subsequent requests use the max_id param to prevent duplicates
        new_tweets = api.user_timeline(screen_name=screen_name, count=200, max_id=oldest)

        # save most recent tweets
        all_tweets.extend(new_tweets)

        # update the id of the oldest tweet less one
        oldest = all_tweets[-1].id - 1

        print("...%s tweets downloaded so far" % (len(all_tweets)))

    favorites = api.get_favorites(screen_name=screen_name, count=200, tweet_mode='extended')
    # We have to do this filtering so we don't mis boy_ebooks into boy_ebooks
    boy_and_people = ["boy_ebooks"] + people
    favorites = [status for status in favorites if status.author.screen_name.lower() not in boy_and_people]

    all_tweets.extend(favorites)

    if os.path.exists(f"/tmp/{screen_name}-clean.txt"):
        os.remove(f"/tmp/{screen_name}-clean.txt")
    clean = open(f"/tmp/{screen_name}-clean.txt", "a", encoding="utf-16")
    bad_words = get_bad_phrases(bucket, key)
    final_list = ""
    for tweet in all_tweets:
        try:
            # This first condition checks if it's a reply
            if hasattr(tweet, "in_reply_to_status_id"):
                if tweet.in_reply_to_status_id is not None:
                    continue
            # Now try and find text if it's a retweet
            if hasattr(tweet, "retweeted_status"):
                if hasattr(tweet.retweeted_status, "truncated") and tweet.retweeted_status.truncated:
                    continue
                if hasattr(tweet, "full_text"):
                    raw = tweet.retweeted_status.full_text
                else:
                    raw = tweet.retweeted_status.text
            elif hasattr(tweet, "full_text"):
                raw = tweet.full_text
            else:
                if hasattr(tweet, "truncated") and tweet.truncated:
                    continue
                raw = tweet.text
        except Exception as e:
            print("Unable to parse tweet")
            raw = ""
        for phrase in bad_words:
            if phrase in raw:
                raw = ""
        cleaned = clean_text(raw)
        if cleaned != "":
            final_list += (cleaned + "\n")
    clean.write(final_list)
    clean.close()
    return final_list


if __name__ == '__main__':
    downloader_function(None, None)
    # get_all_tweets("7e5h")
