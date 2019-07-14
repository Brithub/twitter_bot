# Twitter bot

### About
Hey all, I finally got around to posting the work for my twitter bot, or "Samulation". What it does is takes a file, "cleaned_tweets.txt", which contains the library of tweets, and uses these and some NLP and randomness to automatically tweet every 2 hours or so.


### Files
- cleaned_tweets.txt this (not included) file contains all the tweets you want to generate tweets from, this is a text file containing all tweets to use separated by new lines. I would suggest using a tool like  [tweet dumper](https://github.com/marado/tweet_dumper) to get the needed tweets and using clean_text.py to make the tweets more usable for generation.
- clean_text.py -- This is the main cleanup done in the project. Tweets are in english, and have all kinds of @s, hashtags, and general nonsenses, so this "class" basically tries to clean that up, and makes it more consistent to use in generating tweets
- autoTweet.py -- This is the "main" file, basically it generates and tweets every interval. It should be noted that the parsing and cleaning isn't done in this step to reduce the load on the server. 
- tweet -- this method tweets things, but you gotta have those sysenv set up correctly (Which is a lot of twitter boilerplate not fun)
- generate_ngrams -- this method created bigrams of every word pair in cleaned_tweets, this is used in the generation.
- main -- This is the testing main method, it runs everything and generates some tweets to look at. These aren't tweeted though
- generate.py -- this is what contains the logic for the tweets, note that the current randomly selected tweets is set at 200, the higher this number is, the less derivative the tweets are, but the more nonsensical they might get.

### Why?
For fun 

### How can I run it?

- Either download your csv per request to twitter and use removeExesEtc.py to turn it into cleaned_tweets.txt OR
- Use a tool like [tweet dumper](https://github.com/marado/tweet_dumper) to get all of someone's public tweets and make your own cleaned_tweets.txt
- Make a twitter app (This requires a whole application process takes time)
- Set all the system env variables
- Run main to test if it's generating everything correctly
- Run autoTweet