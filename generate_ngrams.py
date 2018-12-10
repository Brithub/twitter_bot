import pickle
import generate
import nltk
import re

def generate_ngrams():
    path = "cleaned_tweets.txt"
    with open(path, 'r') as file:
        text = file.read()
    tweets = text.split("\n~~~~~~~~~~")



    big = ""
    for line in tweets:
        # print (line)
        big+=line+" TERMINATE "
    tokens = nltk.word_tokenize(big)
    bigrams = nltk.ngrams(tokens, 2)
    trigrams = nltk.ngrams(tokens, 3)


    bigram_dict = {}
    for pair in bigrams:
        key = pair[0].lower() + " " + pair[1].lower()
        key = re.sub("~~~~~~~~~~", "", key)
        if len(pair[0]) <= 15 and len(pair[1]) <= 15 :
            if "terminate" not in pair[0].lower():
                if key.lower() in bigram_dict:
                    bigram_dict[key.lower()] = bigram_dict[key.lower()] + 1
                else:
                    bigram_dict[key.lower()] = 1
    trigram_dict = {}
    for trip in trigrams:
        key = trip[0].lower() + " " + trip[1].lower() + " " + trip[2].lower()
        key = re.sub("~~~~~~~~~~", "", key)
        if len(trip[0]) <= 15 and len(trip[1]) <= 15 :
            if "terminate" not in trip[0].lower():
                if key.lower() in trigram_dict:
                    trigram_dict[key.lower()] = trigram_dict[key.lower()] + 1
                else:
                    trigram_dict[key.lower()] = 1


    unigram_dict = {}
    for word in tokens:
        if word in unigram_dict:
            unigram_dict[word.lower()] = unigram_dict[word.lower()] + 1
        else:
            unigram_dict[word.lower()] = 1

    unigram_dict_cap = {}
    for word in tokens:
        if word in unigram_dict_cap:
            unigram_dict_cap[word] = unigram_dict_cap[word] + 1
        else:
            unigram_dict_cap[word] = 1

    firstWords = []
    for tweet in tweets:
        word = tweet.split(" ")[0]
        if len(word) <=15:
            firstWords.append(word)

    with open('uni.pickle', 'wb') as handle:
        pickle.dump(unigram_dict, handle)

    with open('bi.pickle', 'wb') as handle:
        pickle.dump(bigram_dict, handle)

    with open('tri.pickle', 'wb') as handle:
        pickle.dump(trigram_dict, handle)

    with open('first.pickle', 'wb') as handle:
        pickle.dump(firstWords, handle)

    # for k in sorted(bigram_dict, key=lambda k: bigram_dict[k], reverse=False):
    #     print(k, bigram_dict[k])


