import nltk


def generate_ngrams(tweets):
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
        if len(pair[0]) <= 15 and len(pair[1]) <= 15:
            if "terminate" not in pair[0].lower() and "terminate" not in pair[1].lower():
                if key.lower() in bigram_dict:
                    bigram_dict[key.lower()] = bigram_dict[key.lower()] + 1
                else:
                    bigram_dict[key.lower()] = 1
    trigram_dict = {}
    for trip in trigrams:
        key = trip[0].lower() + " " + trip[1].lower() + " " + trip[2].lower()
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
            firstWords.append(word.lower())


    return bigram_dict,trigram_dict,firstWords


