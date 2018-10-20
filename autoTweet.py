import math
import time
import pickle
import generate
import time
import tweet

while True:

    current_ctime = time.ctime()

    time_time = current_ctime.split(" ")[3].split(":")[0]
    valid_time = 10 <= int(time_time) <= 21

    with open('last.time.pickle', 'rb') as handle:
        old_time = pickle.load(handle)

    if old_time + 7200 < time.time() and valid_time:
        generated = generate.generate()
        tweet.write_tweet(generated)
        print("Tweeted: \"",generated,"\"")

        with open('last.time.pickle', 'wb') as handle:
            pickle.dump(time.time(), handle)
        print("waiting ", 7200, " seconds")
        time.sleep(7200)
    else:
        remaining = 1600
        print("waiting ", remaining, " seconds")
        time.sleep(remaining)

