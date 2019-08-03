import re

import clean_text
import generate_ngrams
import random


def generate_next_word(written, bigram_dict, trigram_dict):
    # use bigrams for the second word
    if written.count(" ") < 2 or random.randint(0, 100) > 85:
        return generate_from_bigrams(written, bigram_dict)
    else:
        return generate_from_trigrams(written, trigram_dict, bigram_dict)


def generate_from_bigrams(prev, bigram_dict):
    last_word = prev.split(" ")[-1]
    nextWords = []
    for pair in bigram_dict:
        if pair.lower().split(" ")[0] == last_word.lower():
            nextWords.append([pair, bigram_dict[pair]])
    if len(nextWords) == 1:
        next_word = nextWords[0][0].split(" ")[1]
    elif len(nextWords) == 0:
        next_word = "RETRYRETRY"
    else:
        candidates = []
        for pair in nextWords:
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

    user = random.randint(0,len(tweets)-1)
    random.shuffle(tweets[user])

    tweet_sample_size = 20

    bigram_dict, trigram_dict, firstWords = generate_ngrams.generate_ngrams(tweets[user][0:tweet_sample_size])

    while True:
        written = ""
        written += firstWords[random.randint(0, len(firstWords) - 1)]

        while "RETRYRETRY" not in written.upper() and "terminate" not in written.lower():
            generated = generate_next_word(written, bigram_dict, trigram_dict)
            written += " " + generated

        if ("RETRYRETRY" not in written.upper()):

            valid = True

            final = re.sub(" terminate| Terminate| TERMINATE", "", written)
            final = final.rstrip()

            final = re.sub(" im ", " I'm ", final)
            final = re.sub(" ive ", " I've ", final)
            final = re.sub(" i ", " I ", final)
            if len(final) > 2:
                final = final[0].capitalize() + final[1:]


            if final.count(" ") > 1 and len(final) <= 85:
                clean_sub = clean_text.clean_text(final[int(.20 * len(final)):int(len(final)*.80)])
                for tweet in tweets[user][0:tweet_sample_size]:
                    if clean_sub.upper() in tweet.upper():
                        valid = False
                        # print ("\nnot tweeting:  ",clean_sub,"\nbecause it is in:  ",tweet,"\n")
            else:
                valid = False

            if valid:
                return final
