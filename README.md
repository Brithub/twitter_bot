# Twitter bot

### About
Hey all, I finally got around to posting the work for my twitter bot, or "Samulation". What it does is takes a file, "cleaned_tweets.txt", which contains the library of tweets, and uses these and some NLP and randomness to automatically tweet every 2 hours or so.


### Files
- clean_text.py -- This is the main cleanup done in the project. Tweets are in english, and have all kinds of @s, hashtags, and general nonsenses, so this function basically tries to clean that up
- tweet -- this method tweets things, but you gotta have those environment variables
- generate_ngrams.py -- this method created bigrams and trigrams of tweets, this is used in the generation.
- preview.py -- This is the testing main method, it runs everything and generates some tweets to look at. These aren't tweeted though. For this to work text files containing sample tweets need to be in a local 'databases' directory
- generate.py -- this is what contains the logic for generating the tweets
- utils.py -- Contains functions used in main.py
- main.py -- This is the function code to be invoked

### Why?
For fun 

### How can I run it?

- This iteration of twitter_bot is actually much more ready out of the box!
- First, get some twitter api keys, (needed for tweeting and downloading tweets), from the twitter api console
- Second, get some ~~lambdas~~ google cloud functions set up using, with the api keys, twitter usernames, and buckets set for environment variables
    - These cloud functions will construct and send tweets, or download the tweets, use methods in main.py as the function code
- And third, use the cloud scheduler to set these functions to be invoked on whatever cadence is wanted
- Then everything should be good to go, completely automated