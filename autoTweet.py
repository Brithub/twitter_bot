import math
import time
import pickle
import generate
import time
import tweet
import os.path

time_pickle_path = 'last.time.pickle'

while True:
    wait_hours = 1
    current_ctime = time.ctime()

    if os.path.isfile(time_pickle_path):

        with open(time_pickle_path, 'rb') as handle:
            old_time = pickle.load(handle)

        if old_time + wait_hours*3600 < time.time():
            generated = generate.generate()
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
        with open(time_pickle_path, 'wb') as handle:
            pickle.dump(0, handle)
