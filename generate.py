import re

import random
import os
import tweet
from utils import list_blobs, get_subject, download_image, get_bad_phrases, clean_text
from google.cloud import storage

bucket = os.environ['BUCKET']

temp_path = "/tmp/badwords.txt"
key = "badwords.txt"


def compose_and_send_tweet(thing, thing2):
    files = list_blobs("twitter_bot_bucket")
    tweets = []

    storage_client = storage.Client("Twitter bot")
    bucket = storage_client.get_bucket("twitter_bot_bucket")

    for user in files:
        if user.name != "badwords.txt":
            blob = bucket.blob(str(user.name))
            blob.download_to_filename(f"/tmp/{user.name}")

            with open(f"/tmp/{user.name}", 'r', encoding="utf-16") as file:
                text = file.read()
            user_tweets = text.split("\n")
            tweets.append(user_tweets)

    generated_tweet = generate(tweets)
    print(generated_tweet)
    subject = get_subject(generated_tweet)
    if len(subject) > 0 and len(subject[0]) > 3 and subject[0][0] != '\'' and random.randint(0, 100) > 60:
        print(f"getting image for: {subject[0]}")
        download_image(subject[0])
        tweet.write_image_tweet(f'/tmp/{subject[0]}.jpg', generated_tweet)
    else:
        print("No nouns found")
        tweet.write_tweet(generated_tweet)
    return generated_tweet


def generate_next_word(written, bigram_dict, trigram_dict):
    # use bigrams for the second word
    if written.count(" ") < 2 or random.randint(0, 100) > 85:
        return generate_from_bigrams(written, bigram_dict)
    else:
        return generate_from_trigrams(written, trigram_dict, bigram_dict)


def generate_from_bigrams(prev, bigram_dict):
    last_word = prev.split(" ")[-1]
    next_words = []
    for pair in bigram_dict:
        if pair.lower().split(" ")[0] == last_word.lower():
            next_words.append([pair, bigram_dict[pair]])
    if len(next_words) == 1:
        next_word = next_words[0][0].split(" ")[1]
    elif len(next_words) == 0:
        next_word = "RETRYRETRY"
    else:
        candidates = []
        for pair in next_words:
            for frequency in range(0, pair[1]):
                candidates.append(pair[0].split(" ")[1])
        random.shuffle(candidates)
        next_word = candidates[0]
    return next_word


def generate_from_trigrams(prev, trigram_dict, bigram_dict):
    if len(prev.split(" ")) < 2:
        return "error"

    old = prev.split(" ")[-1]
    older = prev.split(" ")[-2]

    next_words = []
    for triplet in trigram_dict:
        if triplet.lower().split(" ")[0] + " " + triplet.lower().split(" ")[1] == older.lower() + " " + old.lower():
            next_words.append([triplet, trigram_dict[triplet]])
    if len(next_words) == 1:
        next_word = next_words[0][0].split(" ")[2]
    elif len(next_words) == 0:
        next_word = generate_from_bigrams(prev, bigram_dict)
    else:
        candidates = []
        for pair in next_words:
            for frequency in range(0, pair[1]):
                candidates.append(pair[0].split(" ")[2])
        random.shuffle(candidates)
        next_word = candidates[0]
    return next_word


def generate(tweets):
    user = random.randint(0, len(tweets) - 1)

    bad_phrases = get_bad_phrases(bucket, key)

    tweet_pool = []
    for item in tweets:
        for sub_item in item:
            tweet_pool.append(sub_item)

    while True:
        attempts = 5

        random.shuffle(tweet_pool)
        tweet_sample_size = 30

        bigram_dict, trigram_dict, first_words = generate_ngrams(tweet_pool[0:tweet_sample_size])
        while attempts > 0:
            attempts = attempts - 1
            written = ""
            written += first_words[random.randint(0, len(first_words) - 1)]

            while "RETRYRETRY" not in written.upper() and "terminate" not in written.lower():
                generated = generate_next_word(written, bigram_dict, trigram_dict)
                written += " " + generated

            if "RETRYRETRY" not in written.upper():

                valid = True

                final = re.sub(' terminate| Terminate| TERMINATE', "", written)

                final = final.rstrip()
                if len(final) > 2:
                    final = final[0].capitalize() + final[1:]

                if final.count(" ") > 1 and len(final) <= 120:
                    subset_of_final = " ".join(final.split(" ")[int(len(final.split(" ")) * .40):])
                    for source_tweet in tweet_pool[:tweet_sample_size]:
                        base_words = set(clean_text(source_tweet).upper().split(" "))
                        generated_words = set(clean_text(subset_of_final).upper().split(" "))

                        if generated_words.issubset((base_words)):
                            valid = False
                            # print("not tweeting:  ", final, " because it is in:  ", source_tweet)

                        for phrase in bad_phrases:
                            if phrase.upper() in source_tweet.upper():
                                valid = False
                else:
                    valid = False
                if final.count("\"") != 2 or final.count("\"") != 0:
                    final = re.sub("\"", "", final)
                if valid:
                    return final

def generate_ngrams(tweets):
    big = ""
    for line in tweets:
        big += line + " TERMINATE "
    bigrams = []
    trigrams = []

    words_split = big.split(" ")
    for i in range(0, len(words_split) - 2):
        if words_split[i].lower() != 'terminate':
            bigrams.append([words_split[i], words_split[i + 1]])
            if words_split[i + 1].lower() != 'terminate':
                trigrams.append([words_split[i], words_split[i + 1], words_split[i + 2]])

    bigram_dict = {}
    for pair in bigrams:
        key = pair[0].lower() + " " + pair[1].lower()
        if len(pair[0]) <= 15 and len(pair[1]) <= 15:
            if "terminate" not in pair[0].lower() and "terminate" not in pair[1].lower():
                if key.lower() in bigram_dict:
                    bigram_dict[key.lower()] = bigram_dict[key.lower()] + 1
                else:
                    bigram_dict[key.lower()] = 1
    trigram_dict = {}
    for trip in trigrams:
        key = trip[0].lower() + " " + trip[1].lower() + " " + trip[2].lower()
        if len(trip[0]) <= 15 and len(trip[1]) <= 15:
            if "terminate" not in trip[0].lower():
                if key.lower() in trigram_dict:
                    trigram_dict[key.lower()] = trigram_dict[key.lower()] + 1
                else:
                    trigram_dict[key.lower()] = 1

    unigram_dict = {}
    for word in words_split:
        if word in unigram_dict:
            unigram_dict[word.lower()] = unigram_dict[word.lower()] + 1
        else:
            unigram_dict[word.lower()] = 1

    unigram_dict_cap = {}
    for word in words_split:
        if word in unigram_dict_cap:
            unigram_dict_cap[word] = unigram_dict_cap[word] + 1
        else:
            unigram_dict_cap[word] = 1

    first_words = []
    for tweet in tweets:
        word = tweet.split(" ")[0]
        if len(word) <= 15:
            first_words.append(word.lower())

    return bigram_dict, trigram_dict, first_words


if __name__ == '__main__':
    compose_and_send_tweet(None, None)

