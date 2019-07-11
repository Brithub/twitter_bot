import pickle
import generate
import time
import tweet
import os.path


time.sleep(20)

time_pickle_path = 'last.time.pickle'
print('starting')
path = "cleaned_tweets.txt"
with open(path, 'r') as file:
    text = file.read()
tweets = text.split("\n")
print("cleaned_tweets read")

while True:
    wait_hours = 1.5
    current_ctime = time.ctime()

    if os.path.isfile(time_pickle_path):
        print("time exists")
        with open(time_pickle_path, 'rb') as handle:
            old_time = pickle.load(handle)

        if old_time + wait_hours*3600 < time.time():
            generated = generate.generate(tweets)
            tweet.write_tweet(generated)
            print("Tweeted: \"",generated,"\"")

            with open(time_pickle_path, 'wb') as handle:
                pickle.dump(time.time(), handle)
            print("waiting ", wait_hours*3600, " seconds")
            time.sleep(wait_hours*3600)
        else:
            remaining = wait_hours*1800
            print("waiting ", remaining, " seconds")
            time.sleep(remaining)

    else:
        print('time did not exist')
        time = 1000
        with open(time_pickle_path, 'wb') as handle:
            pickle.dump(time, handle)
