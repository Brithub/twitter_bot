import tweet_dumper
from google.cloud import storage
import datetime
import tweet
import generate
import logging
from utils import delete_blob, upload_blob, list_blobs


def downloader_function(thing,thing2):
    date = (datetime.datetime.utcnow() - datetime.datetime(1970, 1, 1)).days
    people = ["bijanmustard","7e5h","dadurath","daftlimmy","theonion","clickhole"]
    who = people[date % len(people)]
    full = tweet_dumper.get_all_tweets(who)
    logging.info("Got some tweets:" + full[0:300] + "...")
    delete_blob("twitter_bot_bucket",f"{who}-clean.txt")
    upload_blob("twitter_bot_bucket",f"/tmp/{who}-clean.txt",f"{who}-clean.txt")


def compose_and_send_tweet(thing, thing2):
    files = list_blobs("twitter_bot_bucket")
    tweets = []

    storage_client = storage.Client("Twitter bot")
    bucket = storage_client.get_bucket("twitter_bot_bucket")

    for user in files:
        if user.name != "badwords.txt":
            blob = bucket.blob(str(user.name))
            blob.download_to_filename(f"/tmp/{user.name}")

            with open(f"/tmp/{user.name}", 'r', encoding="utf-8") as file:
                text = file.read()
            user_tweets = text.split("\n")
            tweets.append(user_tweets)

    generated_tweet = generate.generate(tweets)
    print(generated_tweet)
    tweet.write_tweet(generated_tweet)
