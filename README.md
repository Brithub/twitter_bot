# Twitter bot

### About
Hey all, I finally got around to posting the work for my twitter bot, or "Samulation". What it does is takes a file, "tweets.csv", parses the csv, cleans some of the text to be at least a little better, then automatically tweets every 2 hours or so.


### Files
- autoTweet.py -- This is the "main" file, basically it generates and tweets every interval. It should be noted that the parsing and cleaning isn't done in this step to reduce the load on the server. 
- removeExesEtc -- This is the main cleanup done in the project. Tweets are in english, and have all kinds of @s, hashtags, and general nonsessne, so this "class" basically tries to clean that up, and put it into a nicer looking file named "cleaned_tweets.txt"
- tweet -- this method tweets things, but you gotta have those sysenv set up correctly (Which is a lot of twitter boilerplate not fun)
- generate_ngrams -- this method created bigrams of every word pair in cleaned_tweets, this is used in the generation.
- main -- This is the testing main method, it runs everything and generates ten tweets to look at. These aren't tweeted though

### Why?
For fun 

### How can I run it?
oof, if you really want to, all you have to do is:
- download your csv per request to twitter
- Make a twitter app (This requires a whole application process takes time)
- Set all the system env variables
- Run main
- Run autoTweet I guess