# Twitter bot

### About
Hey all, here's the code for my twitter bot. It uses google cloud functions to scrape tweets, and generate nonsense using that data. It's not perfect but it's at least fun:)

### Files
- tweet -- this method tweets things, but you gotta have those environment variables
- generate_ngrams.py -- this method created bigrams and trigrams of tweets, this is used in the generation.
- generate.py -- This is what contains the logic for generating and sending tweets
- utils.py -- Contains a whole bunch of helper logic

### Why?
For fun 

### How can I run it?

- This iteration of twitter_bot is actually much more ready out of the box!
- First, get some twitter api keys, (needed for tweeting and downloading tweets), from the twitter api console
- Second, get some ~~lambdas~~ google cloud functions set up using, with the api keys, twitter usernames, and buckets set for environment variables
    - These cloud functions will construct and send tweets, or download the tweets, use methods in main.py as the function code
- And third, use the cloud scheduler to set these functions to be invoked on whatever cadence is wanted
- Then everything should be good to go, completely automated